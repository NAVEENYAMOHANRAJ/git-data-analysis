from typing import List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.models import PullRequest, Contributor, Repository
from sqlalchemy import func

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_open_pr_count(self, repo_id: int) -> int:
        return self.db.query(PullRequest).filter(
            PullRequest.repo_id == repo_id,
            PullRequest.state == "OPEN"
        ).count()
    
    def get_stale_pr_count(self, repo_id: int, days: int = 30) -> int:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return self.db.query(PullRequest).filter(
            PullRequest.repo_id == repo_id,
            PullRequest.state == "OPEN",
            PullRequest.created_at < cutoff_date
        ).count()
    
    def get_avg_cycle_time(self, repo_id: int) -> float:
        result = self.db.query(func.avg(PullRequest.cycle_time_days)).filter(
            PullRequest.repo_id == repo_id,
            PullRequest.cycle_time_days.isnot(None)
        ).scalar()
        return round(result or 0, 2)
    
    def get_median_cycle_time(self, repo_id: int) -> float:
        prs = self.db.query(PullRequest.cycle_time_days).filter(
            PullRequest.repo_id == repo_id,
            PullRequest.cycle_time_days.isnot(None)
        ).all()
        
        if not prs:
            return 0
        
        values = sorted([p[0] for p in prs])
        n = len(values)
        return values[n // 2] if n % 2 == 1 else (values[n // 2 - 1] + values[n // 2]) / 2
    
    def get_merge_rate(self, repo_id: int) -> float:
        merged = self.db.query(PullRequest).filter(
            PullRequest.repo_id == repo_id,
            PullRequest.state == "MERGED"
        ).count()
        
        closed = self.db.query(PullRequest).filter(
            PullRequest.repo_id == repo_id,
            PullRequest.state.in_(["MERGED", "CLOSED"])
        ).count()
        
        return round((merged / closed * 100) if closed > 0 else 0, 2)
    
    def get_avg_review_duration(self, repo_id: int) -> float:
        result = self.db.query(func.avg(PullRequest.review_duration_hours)).filter(
            PullRequest.repo_id == repo_id,
            PullRequest.review_duration_hours.isnot(None)
        ).scalar()
        return round((result or 0) / 24, 2)  # Convert to days
    
    def get_avg_wait_for_review(self, repo_id: int) -> float:
        result = self.db.query(func.avg(PullRequest.wait_for_review_hours)).filter(
            PullRequest.repo_id == repo_id,
            PullRequest.wait_for_review_hours.isnot(None)
        ).scalar()
        return round((result or 0) / 24, 2)  # Convert to days
    
    def get_pr_throughput(self, repo_id: int, weeks: int = 4) -> Dict[str, int]:
        """PRs merged per week"""
        cutoff_date = datetime.utcnow() - timedelta(weeks=weeks)
        
        prs = self.db.query(PullRequest).filter(
            PullRequest.repo_id == repo_id,
            PullRequest.merged_at >= cutoff_date
        ).all()
        
        throughput = {}
        for pr in prs:
            week = pr.merged_at.strftime("%Y-W%U")
            throughput[week] = throughput.get(week, 0) + 1
        
        return throughput
    
    def get_monthly_pr_flow(self, repo_id: int, months: int = 3) -> Dict[str, Dict[str, int]]:
        """Created vs merged vs closed PRs by month"""
        cutoff_date = datetime.utcnow() - timedelta(days=30 * months)
        
        prs = self.db.query(PullRequest).filter(
            PullRequest.repo_id == repo_id,
            PullRequest.created_at >= cutoff_date
        ).all()
        
        flow = {}
        for pr in prs:
            month = pr.created_at.strftime("%Y-%m")
            if month not in flow:
                flow[month] = {"created": 0, "merged": 0, "closed": 0}
            
            flow[month]["created"] += 1
            if pr.state == "MERGED":
                flow[month]["merged"] += 1
            elif pr.state == "CLOSED":
                flow[month]["closed"] += 1
        
        return flow
    
    def get_oldest_open_prs(self, repo_id: int, limit: int = 10) -> List[Dict]:
        prs = self.db.query(PullRequest).filter(
            PullRequest.repo_id == repo_id,
            PullRequest.state == "OPEN"
        ).order_by(PullRequest.created_at.asc()).limit(limit).all()
        
        return [
            {
                "number": pr.pr_number,
                "title": pr.title,
                "created_at": pr.created_at.isoformat() if pr.created_at else None,
                "age_days": (datetime.utcnow() - pr.created_at).days if pr.created_at else 0,
                "author": pr.author,
                "review_count": pr.review_count
            }
            for pr in prs
        ]
    
    def get_slowest_merged_prs(self, repo_id: int, limit: int = 10) -> List[Dict]:
        prs = self.db.query(PullRequest).filter(
            PullRequest.repo_id == repo_id,
            PullRequest.state == "MERGED",
            PullRequest.cycle_time_days.isnot(None)
        ).order_by(PullRequest.cycle_time_days.desc()).limit(limit).all()
        
        return [
            {
                "number": pr.pr_number,
                "title": pr.title,
                "cycle_time_days": pr.cycle_time_days,
                "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
                "author": pr.author,
                "review_count": pr.review_count,
                "files_changed": pr.files_changed
            }
            for pr in prs
        ]
    
    def get_contributor_activity(self, repo_id: int) -> List[Dict]:
        contributors = self.db.query(Contributor).filter(
            Contributor.repo_id == repo_id
        ).all()
        
        return [
            {
                "username": c.username,
                "total_prs": c.total_prs,
                "merged_prs": c.merged_prs,
                "avg_cycle_time": round(c.avg_cycle_time, 2),
                "avg_wait_for_review": round(c.avg_review_time / 24, 2) if c.avg_review_time else 0,  # Convert hours to days
                "merge_rate": round((c.merged_prs / c.total_prs * 100) if c.total_prs > 0 else 0, 2),
                "stale_pr_count": c.stale_pr_count
            }
            for c in contributors
        ]
    
    def get_median_cycle_time_rounded(self, repo_id: int) -> float:
        """Get median cycle time rounded to 1 decimal"""
        return round(self.get_median_cycle_time(repo_id), 1)
    
    def get_avg_reviews_per_pr(self, repo_id: int) -> float:
        """Average number of reviews per PR"""
        result = self.db.query(func.avg(PullRequest.review_count)).filter(
            PullRequest.repo_id == repo_id,
            PullRequest.review_count.isnot(None)
        ).scalar()
        return round(result or 0, 1)
    
    def get_kpi_summary(self, repo_id: int) -> Dict[str, Any]:
        return {
            "open_prs": self.get_open_pr_count(repo_id),
            "stale_prs": self.get_stale_pr_count(repo_id),
            "avg_cycle_time": self.get_avg_cycle_time(repo_id),
            "median_cycle_time": self.get_median_cycle_time_rounded(repo_id),
            "avg_wait_for_review": self.get_avg_wait_for_review(repo_id),
            "avg_review_duration": self.get_avg_review_duration(repo_id),
            "merge_rate": self.get_merge_rate(repo_id),
            "avg_reviews_per_pr": self.get_avg_reviews_per_pr(repo_id),
        }

from datetime import datetime

from sqlalchemy.orm import Session as DBSession

from app.models.session import Session as SessionModel
from app.models.behavioral_state import BehavioralState


class BehavioralEngine:
    """Single source of truth for session aggregation and behavioral scores."""

    @staticmethod
    def compute_and_update(user_id: str, db: DBSession) -> BehavioralState:
        """
        Aggregates session data and upserts BehavioralState.
        Persists zeroed aggregates when the user has no sessions.
        """
        sessions = (
            db.query(SessionModel)
            .filter(SessionModel.user_id == user_id)
            .all()
        )

        state = (
            db.query(BehavioralState)
            .filter(BehavioralState.user_id == user_id)
            .first()
        )

        if not state:
            state = BehavioralState(user_id=user_id)
            db.add(state)

        if not sessions:
            state.total_sessions = 0
            state.total_focus_minutes = 0
            state.avg_session_length = 0.0
            state.interruption_rate = 0.0
            state.efficiency_score = 0.0
            state.burnout_risk_score = 0.0
            state.focus_consistency_score = 0.0
            state.predicted_daily_capacity_minutes = 0.0
            state.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(state)
            return state

        total_sessions = len(sessions)
        total_focus_minutes = sum(s.duration_minutes for s in sessions)
        avg_session_length = total_focus_minutes / total_sessions

        interruption_total = sum(s.interruption_count for s in sessions)
        interruption_rate = interruption_total / total_sessions

        efficiency_score = min((avg_session_length / 45) * 100, 100)
        burnout_risk_score = min(interruption_rate * 20, 100)
        focus_consistency_score = max(0, 100 - burnout_risk_score)
        predicted_daily_capacity_minutes = avg_session_length * 6

        state.total_sessions = total_sessions
        state.total_focus_minutes = total_focus_minutes
        state.avg_session_length = avg_session_length
        state.interruption_rate = interruption_rate
        state.efficiency_score = efficiency_score
        state.burnout_risk_score = burnout_risk_score
        state.focus_consistency_score = focus_consistency_score
        state.predicted_daily_capacity_minutes = predicted_daily_capacity_minutes
        state.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(state)
        return state

    @staticmethod
    def get_analytics(user_id: str, db: DBSession) -> BehavioralState:
        """Recompute and return persisted behavioral state (always fresh)."""
        return BehavioralEngine.compute_and_update(user_id, db)

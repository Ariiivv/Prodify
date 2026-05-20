from sqlalchemy.orm import Session as DBSession

from app.models.session import Session as SessionModel
from app.models.behavioral_state import BehavioralState


class BehavioralEngine:

    @staticmethod
    def compute_and_update(user_id: str, db: DBSession):
        """
        Aggregates session data → updates BehavioralState
        """

        sessions = db.query(SessionModel).filter(
            SessionModel.user_id == user_id
        ).all()

        if not sessions:
            return None

        total_sessions = len(sessions)
        total_focus_minutes = sum(s.duration_minutes for s in sessions)

        avg_session_length = total_focus_minutes / total_sessions

        interruption_total = sum(s.interruption_count for s in sessions)
        interruption_rate = interruption_total / total_sessions

        # SIMPLE heuristics (no AI yet, safe baseline)
        efficiency_score = min((avg_session_length / 45) * 100, 100)

        burnout_risk = min(interruption_rate * 20, 100)

        focus_consistency = max(0, 100 - burnout_risk)

        predicted_capacity = avg_session_length * 6  # rough daily estimate

        state = db.query(BehavioralState).filter(
            BehavioralState.user_id == user_id
        ).first()

        if not state:
            state = BehavioralState(user_id=user_id)
            db.add(state)

        state.total_sessions = total_sessions
        state.total_focus_minutes = total_focus_minutes
        state.avg_session_length = avg_session_length
        state.interruption_rate = interruption_rate

        state.efficiency_score = efficiency_score
        state.burnout_risk_score = burnout_risk
        state.focus_consistency_score = focus_consistency
        state.predicted_daily_capacity_minutes = predicted_capacity

        db.commit()
        db.refresh(state)

        return state
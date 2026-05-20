"""Smoke tests: health check and full productivity entity create chain."""


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200


def test_create_chain_and_analytics(client):
    user = client.post(
        "/users",
        json={"email": "smoke@prodify.test", "name": "Smoke User"},
    )
    assert user.status_code == 201
    user_id = user.json()["id"]

    workspace = client.post(
        "/workspaces",
        json={"name": "Deep Work", "user_id": user_id},
    )
    assert workspace.status_code == 201
    workspace_id = workspace.json()["id"]

    work_item = client.post(
        "/work-items",
        json={
            "title": "Backend Phase A",
            "type": "one_time",
            "user_id": user_id,
            "workspace_id": workspace_id,
        },
    )
    assert work_item.status_code == 201
    work_item_id = work_item.json()["id"]

    task = client.post(
        "/tasks",
        json={"work_item_id": work_item_id, "title": "Alembic setup"},
    )
    assert task.status_code == 201
    task_id = task.json()["id"]

    session = client.post(
        "/sessions",
        json={
            "user_id": user_id,
            "task_id": task_id,
            "duration_minutes": 45,
            "interruption_count": 1,
            "focus_score": 85.0,
        },
    )
    assert session.status_code == 201
    assert session.json()["interruption_count"] == 1

    analytics = client.get(f"/users/{user_id}/analytics")
    assert analytics.status_code == 200
    body = analytics.json()
    assert body["total_sessions"] == 1
    assert body["total_focus_minutes"] == 45
    assert body["efficiency_score"] > 0
    assert "burnout_risk_score" in body


def test_work_item_workspace_ownership_mismatch(client):
    user_a = client.post(
        "/users",
        json={"email": "a@prodify.test", "name": "A"},
    ).json()
    user_b = client.post(
        "/users",
        json={"email": "b@prodify.test", "name": "B"},
    ).json()
    workspace_a = client.post(
        "/workspaces",
        json={"name": "A Workspace", "user_id": user_a["id"]},
    ).json()

    response = client.post(
        "/work-items",
        json={
            "title": "Invalid",
            "type": "one_time",
            "user_id": user_b["id"],
            "workspace_id": workspace_a["id"],
        },
    )
    assert response.status_code == 403


def test_analytics_unknown_user_returns_404(client):
    response = client.get("/users/nonexistent-user-id/analytics")
    assert response.status_code == 404

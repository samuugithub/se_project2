from unittest.mock import patch
import notification_watcher

@patch("notification_watcher.get_connection")
@patch("notification_watcher.send_alert")
def test_check_new_alerts(mock_send_alert, mock_conn):
    class FakeCursor:
        def execute(self, *a, **k): pass
        def fetchone(self): return {"prediction_id": 10, "system_id": "SYS1", "probability": 95}
        def close(self): pass

    class FakeDB:
        def cursor(self, dictionary=True): return FakeCursor()
        def close(self): pass

    mock_conn.return_value = FakeDB()
    notification_watcher.last_id = 0
    notification_watcher.check_new_alerts()
    mock_send_alert.assert_called_once()

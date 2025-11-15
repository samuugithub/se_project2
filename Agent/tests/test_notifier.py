from unittest.mock import patch, MagicMock
import notifier

@patch("notifier.get_connection")
def test_get_admin_contacts_returns_empty(mock_conn):
    mock_conn.side_effect = Exception("DB error")
    result = notifier.get_admin_contacts()
    assert result == []

from django.test import TestCase


class TestValidateTelegramMiniAppData(TestCase):
    def setUp(self):
        self.init_data_1 = "query_id=AAHXv_03AAAAANe__TfVCFD_&user=%7B%22id%22%3A939376599%2C%22first_name%22%3A%22arterrr%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22artertendean%22%2C%22language_code%22%3A%22en%22%2C%22is_premium%22%3Atrue%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1723083100&hash=83dae1980c08b7706c4f572eef937c10f885101eb1f56848203ba88e7cd708ec"
        self.init_data_2 = "query_id=AAHXv_03AAAAANe__TfVCFD_&user=%7B%22id%22%3A939376599%2C%22first_name%22%3A%22arterrr%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22artertendean%22%2C%22language_code%22%3A%22en%22%2C%22is_premium%22%3Atrue%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1723083100&hash=83dae1980c08b7706c4f572eef937c10f885101eb1f56848203ba88e7cd708ecinvalid"

    def test_validate_mini_app_data_success(self):
        data = {"init_data": self.init_data_1}
        response = self.client.post(
            "/twitter-downloader/telegram-webhook/validate-mini-app-data/", data, format="json"
        )
        self.assertEqual(response.status_code, 200, "Should return 200 OK")

    def test_validate_mini_app_data_failed(self):
        data = {"init_data": self.init_data_2}
        response = self.client.post(
            "/twitter-downloader/telegram-webhook/validate-mini-app-data/", data, format="json"
        )
        self.assertEqual(response.status_code, 400, "Should return 400 Bad Request")

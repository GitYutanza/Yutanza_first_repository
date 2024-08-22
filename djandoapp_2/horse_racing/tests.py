from django.test import TestCase
from horse_racing.models import RaceResult
from horse_racing.scraype import scrape

class ScrapeTests(TestCase):
    def setUp(self):
        # テストデータベースの初期化
        RaceResult.objects.all().delete()

    def test_scrape_race_results(self):
        # スクレイピング処理の実行
        scrape()

        # スクレイピング結果がデータベースに保存されているかを確認
        results_count = RaceResult.objects.count()
        self.assertGreater(results_count, 0, "No data was scraped and saved into the database.")

        # テスト用にいくつかのデータを検証する
        example_result = RaceResult.objects.first()
        self.assertIsNotNone(example_result.race_id, "Race ID should not be None")
        self.assertIsNotNone(example_result.horse_name, "Horse Name should not be None")
        self.assertIsNotNone(example_result.jockey_name, "Jockey Name should not be None")
        self.assertIsInstance(example_result.race_date, object, "Race Date should be a valid date object")

    def tearDown(self):
        # テスト後にデータベースをクリア
        RaceResult.objects.all().delete()

# Create your tests here.

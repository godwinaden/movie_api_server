import time


class TestAPIs:
    def test_create_movie(self):
        start_time = time.time()
        completed_in: str = str((time.time() - start_time)) % ' Seconds'
        print(f"The function was completed in {completed_in}")

    # def test_create
    
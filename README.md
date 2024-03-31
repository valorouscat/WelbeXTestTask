## How to run
For run containers: `docker-compose up`

## Some info about used algorithm
For calculation I've used annealing simulation algorithm which might be not absolutely correct all times, but its fast and decent method to resolve commivoyager problem. By default I used following initial params of the system: `temp=100`, `cooling_rate=0.003`, `stop_temp=0.001`. But you can correct them in `utils.simulated_annealing` function.

## Tests
I've put some trivial unittests in `tests.py` but nothing special, because creating some meaningful tests will take a long time.

## How to make this API trully RESTful
- It's better to use different endpoint for csv file upload
- Use headers data to convey some metadata (for example in prod we want to add some sort of security and jwt is good option for this)
- We also may add some PUT or DELETE to modify and delete routes 
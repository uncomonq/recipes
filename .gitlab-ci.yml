stages:
  - lint
  - black

flake8_check:
  stage: lint
  script:
    - pip install -r requirements/test.txt
    - flake8 .

black_check:
  stage: black
  image: registry.gitlab.com/pipeline-components/black:latest
  script:
    - black --check .


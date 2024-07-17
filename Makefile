build:
	@docker build -t cogbot .

run: build
	@docker run -v ./data:/CogBot/data cogbot 
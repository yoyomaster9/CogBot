build:
	@docker build -t cogbot .

run: build
	@docker run -d -v ./data:/CogBot/data cogbot 
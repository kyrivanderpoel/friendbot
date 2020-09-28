provider "aws" {
  region = "us-east-1"
}

variable "open_weather_map_api_key" {
  type        = string
  description = "A valid Open Weather Map API key."
}

variable "discord_bot_token" {
  type        = string
  description = "The token from Discord that is used to execute the bot."
}

data "aws_ami" "amazon-linux-2" {
  most_recent = true
  owners = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-ebs"]
  }
}

resource "aws_instance" "friendbot" {
  ami           = data.aws_ami.amazon-linux-2.id
  instance_type = "t2.micro"
  user_data = templatefile("${path.module}/user-data.sh.tpl", {
    open_weather_map_api_key = var.open_weather_map_api_key
    discord_bot_token = var.discord_bot_token
  })

  tags = {
    Name = "friendbot"
  }
}

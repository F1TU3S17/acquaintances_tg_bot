import os
from environs import Env

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
admin_id = env.int('ADMIN_ID')


# ----------------------------------------------- #
# Plugin Name           : TradingView-Webhook-Bot #
# Author Name           : vsnz                    #
# File Name             : handler.py              #
# ----------------------------------------------- #

import config
from telegram import Bot
from discord_webhook import DiscordWebhook, DiscordEmbed
from slack_webhook import Slack
import tweepy
import smtplib, ssl
from email.mime.text import MIMEText

def send_alert(data):
    if config.send_telegram_free_alerts:
        tg_bot = Bot(token=config.tg_free_token)
        if "FREE Signal" in data['msg']:
            try:
                tg_bot.sendMessage(data['telegram'], data['msg'].encode('latin-1','backslashreplace').decode('unicode_escape'), parse_mode='MARKDOWN')
            except KeyError:
                tg_bot.sendMessage(config.tg_free_channel, data['msg'].encode('latin-1','backslashreplace').decode('unicode_escape'), parse_mode='MARKDOWN')
            except Exception as e: 
                print('[X] Telegram Error:\n>', e)
            
    if config.send_telegram_vip_alerts:
        tg_bot = Bot(token=config.tg_vip_token)
        try:
            tg_bot.sendMessage(data['telegram'], data['msg'].encode('latin-1','backslashreplace').decode('unicode_escape'), parse_mode='MARKDOWN')
        except KeyError:
            tg_bot.sendMessage(config.tg_vip_channel, data['msg'].encode('latin-1','backslashreplace').decode('unicode_escape'), parse_mode='MARKDOWN')
        except Exception as e: 
            print('[X] Telegram Error:\n>', e)
            
    if config.send_discord_alerts:
        try:
            webhook = DiscordWebhook(url="https://discord.com/api/webhooks/" + data['discord'])
            embed = DiscordEmbed(title=data['msg'])
            webhook.add_embed(embed)
            response = webhook.execute()
        except KeyError:
            webhook = DiscordWebhook(url="https://discord.com/api/webhooks/" + config.discord_webhook)
            embed = DiscordEmbed(title=data['msg'])
            webhook.add_embed(embed)
            response = webhook.execute()
        except Exception as e: 
            print('[X] Discord Error:\n>', e)

    if config.send_slack_alerts:
        try:
            slack = Slack(url='https://hooks.slack.com/services/' + data['slack'])
            slack.post(text=data['msg'])
        except KeyError:
            slack = Slack(url='https://hooks.slack.com/services/' + config.slack_webhook)
            slack.post(text=data['msg'])
        except Exception as e: 
            print('[X] Slack Error:\n>', e)

    if config.send_twitter_alerts:
        tw_auth = tweepy.OAuthHandler(config.tw_ckey, config.tw_csecret)
        tw_auth.set_access_token(config.tw_atoken, config.tw_asecret)
        tw_api = tweepy.API(tw_auth)
        try:
            tw_api.update_status(status=data)
        except Exception as e:
            print('[X] Twitter Error:\n>', e)
        
    if config.send_email_alerts:
        try:
            email_msg = MIMEText(data)
            email_msg['Subject'] = config.email_subject
            email_msg['From']    = config.email_sender
            email_msg['To']      = config.email_sender
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(config.email_host, config.email_port, context=context) as server:
                server.login(config.email_user, config.email_password)
                server.sendmail(config.email_sender, config.email_receivers, email_msg.as_string())
                server.quit()
        except Exception as e:
            print('[X] Email Error:\n>', e)

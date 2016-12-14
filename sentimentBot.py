# This example show how to write an inline mode telegramt bot use pyTelegramBotAPI.
import telebot
import time
import sys
import logging
from telebot import types
import rpy2.robjects as ro
from rpy2.robjects.packages import importr


API_TOKEN = 'Yourtoken'

bot = telebot.TeleBot(API_TOKEN)
telebot.logger.setLevel(logging.DEBUG)
extremes = importr('syuzhet')
codigo_r_library = """
libreryLoad <- function(name) {
    requiredPackages = c(name)
    for(p in requiredPackages){
      if(!require(p,character.only = TRUE)) install.packages(p,repos="http://cran.rstudio.com/")
      library(p,character.only = TRUE)
    }
}
"""
ro.r(codigo_r_library);
codigo_r = """
resultSent <- function(cadena) {
  vectorS<-get_nrc_sentiment(cadena);
  yourText<-paste("Your text: ",cadena);
  anger<-paste("Anger: ",vectorS$anger);
  anticipation<-paste("Anticipation: ",vectorS$anticipation);
  disgust<-paste("Disgust: ",vectorS$disgust);
  fear<-paste("Fear: ",vectorS$fear);
  joy<-paste("Joy: ",vectorS$joy);
  sadness<-paste("Sadness: ",vectorS$sadness);
  surprise<-paste("Surprise: ",vectorS$surprise);
  trust<-paste("Trust: ",vectorS$trust);
  negative<-paste("Negative: ",vectorS$negative);
  positive<-paste("Positive: ",vectorS$positive);
  totalResult<-paste(yourText,negative,trust,surprise,sadness,joy,fear,disgust,anticipation,anger,sep="\n")
  return(totalResult)
}
"""
ro.r(codigo_r);
loadLib = ro.globalenv['libreryLoad'];
loadLib('syuzhet');
resultSent_py = ro.globalenv['resultSent'];


@bot.inline_handler(lambda query: query.query != '')
def query_text(inline_query):
    try:
        res = resultSent_py(inline_query.query);
        textOut=res[0];
        r = types.InlineQueryResultArticle('1', 'View score', types.InputTextMessageContent(textOut))
        
        bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)




#bot.inline_handler(lambda query: len(query.query) is 0)
def default_query(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'waiting', types.InputTextMessageContent('waiting'))
        bot.answer_inline_query(inline_query.id, [r])
    except Exception as e:
        print(e)


def main_loop():
    bot.polling(True)
    while 1:
        time.sleep(3)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)

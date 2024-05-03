import logging
import string
import datetime
import re
import random
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
'"Logs chat events"'
postingdict={}
"'Posting dict starts empty by default, will contain postings by adding the person's name as a sub dictionary within the dictionary"

rawdate=datetime.date.today()

formdate= rawdate.strftime('%d/%m/%Y')
#added date function here so that postings will automatically get removed once it expires

wholesomemsg=["Have a nice day!", "ORD is but a mindset", "The SIT room needs some cleaning", "At the end of the day, the day ends", f"Today's date is {formdate}", "This bot was created by 3SG Benny", "Posted out after 2 months, sike I'm back ~SCT Ethan","Same shit different toilet ~ 3SG(NS) Fan" ]
#for fun
no_punc = str.maketrans('', '', "[],'{}")
print(wholesomemsg[4])

adminlist=set()
"'Admin list is the list of administrators for this bot. All those given the admin password listed below can become admin'"
password=['P@ssword_12345']
#does not require source code editing to change password

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Welcome to beautiful Sembawang!')
#basic starting message all sits will see
    
async def newsit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type=update.message.chat.type
    inpro_details=str(f"""Rank/ Name (all caps):
Full NRIC:
Status: Completed Course / OOC / OOT
Mobile Number:
Frame: CLX FXXX
Date of Completed Course / OOC / OOT: XX/XX/2023
Date of Posted In: XX/XX/2023
Age: XX
NOK Name/Relationship:
NOK Contact:
License Number (if any):
DRC(if any):""")
    if chat_type=='private':
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Please fill this message with the information required. Take note NOK stands for Next of Kin (i.e. your parents/relatives).Please delete what ever is NOT applicable for status and date of completed course/ooc/oot. After you are done, send the completed message back to the bot.\n{(inpro_details)}')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Please PM me this command!')
#Command that helps gather basic info and forwards it to ALL admins in the list. Changed it to PM only as sending in the group will lead to data issues
        
async def rules (update: Update, context: ContextTypes.DEFAULT_TYPE):
    rules= 'This are the rules you must follow, any one caught breaking the rules will receive punishment.\n1. Be punctual when reporting to SIT room. \n2. Keep your bearings in tip top condition, such as hair, uniform, fingernails. Headphones are allowed ONLY within the SIT room \n3. Keep the SIT room neat and tidy by all times. \n4. Treat your superiors with respect. \n5. Do not use the toilets on level 2.'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=rules)
#can only edit in source code, but this isnt very important
    
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Check out the list of commands available. To view posting, use the command /viewposting. For new SITs reporting, please use the command /newsit. For rules to follow while being an SIT, please use the command /rules')

async def addposting (update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user: str = update.message.chat.id
    if effective_user in adminlist:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Posting Template:\n Posting Name: Unit: Date: Vocation: \n IF YOU WANT THE POSTING DATE TO WORK GIVE IT IN DD/MM/YYYY!!!!')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='You have no permission to use this command. Your name and chatid has been logged, please contact the administrator for more info')
#Take note of the fact that YOU MUST GIVE IT DD/MM/YYYY, other formats will be rejected!!!! This is to faciliate auto deletion of posting
        
async def deleteposting (update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user: str = update.message.chat.id
    #this line is for auto deleting once posting date expires
    for key in list(postingdict):
        if postingdict[key]["Date"]<formdate:
            postingdict.pop(key)
            print("Posting outdated, deleted")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'The posting, {key}, was deleted as it was outdated')
    if effective_user in adminlist:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Please delete the posting in exactly this format: "delete [name]"')
        #manual deleting is possible
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='You have no permission to use this command. Your name and chatid has been logged, please contact the administrator for more info')
        #empty threat unless you check the logs on time

async def admin (update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user: str = update.message.chat.id
    text: str = update.message.text
    split=text.split(' ')
    print(text)
    psswdstr=str(password)
    psswd=psswdstr.translate(no_punc)
    try:
        if psswd == split[1]:
            adminlist.add(effective_user)
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Given admin rights whoohoo')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Wrong Password')

    except IndexError:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='You did not type a password after "/admin"')
  
#to use, type /admin [Password]
        
async def demote (update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user: str = update.message.chat.id
    if effective_user in adminlist:
        adminlist.discard(effective_user)
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Removed admin rights')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='You have no permission to use this command. Your name and chatid has been logged, please contact the administrator for more info')
#demotes yourself only, there is a text command which resets admin list (in case someone random gets admin)
        
async def viewposting (update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    effective_user: str = update.message.chat.id
    postingstr=str()
    postingclean=str()
    for key in postingdict:
        postingstr= postingstr + 'Name: '+ key + ' '+ str(postingdict[key]) + f'\n'+f'\n'
    postingclean = postingstr.translate(no_punc)
    if effective_user == -1002031144727:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Complete list of posting shown below:\n{(postingclean)}')
    if effective_user in adminlist:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Complete list of posting shown below:\n{(postingclean)}')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'For security and data privacy reasons, this command only works in the SIT chat, please use this command in the SIT telegram chat.')
#added data security protection by making it a SIT group chat only command
    
async def wholesome_message (update: Update, context: ContextTypes.DEFAULT_TYPE):
    wholemsg=random.choice(wholesomemsg)
    wholemsgprocessed=wholemsg.translate(no_punc)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{wholemsgprocessed}')

async def reset_wholesome_message (update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_user: str = update.message.chat.id
    msgno= 1

    if effective_user in adminlist:
        for i in wholesomemsg:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Message no. {msgno} is {i} ')
            msgno+=1
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'To delete a message simply type "remove quote [quote number]", remove the square brackets')     
#auto adjusts quote no.
        
async def sit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    processed: str = text.lower()
    effective_user: str = update.message.chat.id

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    print (f'{effective_user}')
#find your chat ID below, and copy the number here according to the format here
    if effective_user == 978049867 or 640072239:
        if processed == 'view admin':
            await context.bot.send_message(chat_id=update.effective_chat.id, text=str(adminlist))
        if 'change password' in processed:
            all_words = update.message.text.split(' ')
            password.append(all_words[2])
            password.pop(0)
            await context.bot.send_message (chat_id=update.effective_chat.id, text=f'Password Updated. {(password)}')
        if processed == 'reset all admin':
            adminlist.clear()
            adminliststr=str(adminlist)
            await context.bot.send_message (chat_id=update.effective_chat.id, text=f'Cleared all admin {(adminliststr)}')
#allows certain users in the admin list to change password and reset admin, for obvious reasons not all can do it. Will require a source code change every few years so not big issue I believe
#if for some reason the future specs do not change master admins then usually wont be the biggest of issues
    if effective_user in adminlist:
        all_words = update.message.text.split(' ')
        print (all_words)
        if 'posting' in processed:
            if len(all_words)<5:
                await context.bot.send_message (chat_id=update.effective_chat.id, text='INFO INCOMPLETE!')
            if 'name:' and 'unit:' and 'date:' and 'vocation:' in processed:
                nameindex=all_words.index('Name:')
                unitindex=all_words.index('Unit:')
                dateindex=all_words.index('Date:')
                vocindex=all_words.index('Vocation:')

                name=str(all_words[nameindex+1:unitindex])
                name_processed= name.translate(no_punc)
                unit=str(all_words[unitindex+1:dateindex])
                unit_processed= unit.translate(no_punc)
                date=str (all_words[dateindex+1:vocindex])
                try:
                    date_obj=datetime.datetime.strptime(date.translate(no_punc), '%d/%m/%Y')
                    date_obj_processed=date_obj.strftime('%d/%m/%Y')
                except:
                    await context.bot.send_message (chat_id=update.effective_chat.id, text='ERROR: INCORRECT DATE FORMAT. DATE MUST BE IN "DD/MM/YYYY" FORMAT, ZEROES INCLUDED')
#try makes this place fail gracefully in case something is wrong
                voc=str(all_words[vocindex+1:])
                voc_processed=voc.translate (no_punc)
                try:
                    postingdict[name_processed]={"Posted Unit":unit_processed, "Date":date_obj_processed, "Vocation":voc_processed}
                    print (postingdict)
                except:
                    await context.bot.send_message (chat_id=update.effective_chat.id, text='Something is wrong with your input')
                else:
                    await context.bot.send_message (chat_id=update.effective_chat.id, text='Posting Added OwO')
            else:
                await context.bot.send_message (chat_id=update.effective_chat.id, text='Something is wrong with your input')

        if 'delete' in processed[0:8]:
            if 'all' in processed[7:]:
                postingdict.clear()
                await context.bot.send_message (chat_id=update.effective_chat.id, text=f'Removed all postings')
            else:

                name=str (all_words[1:])
                name_processed= name.translate(no_punc)
                try:
                    postingdict.pop (name_processed)
                except:
                    await context.bot.send_message (chat_id=update.effective_chat.id, text='Something went wrong')
                else:
                    await context.bot.send_message (chat_id=update.effective_chat.id, text='Posting Deleted :(')
        if 'add this quote' in processed:
            pattern=re.compile("add this quote", re.IGNORECASE)
            quote=pattern.sub("",text)
            wholesomemsg.append(quote)
            await context.bot.send_message (chat_id=update.effective_chat.id, text=f'Added quote:{quote}')
        if 'remove quote' in processed:
            quotenoraw=all_words[2]
            quotenop=quotenoraw.translate(no_punc)
            quoteno= int(quotenop)-1
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Removed quote {wholesomemsg[quoteno]}')
            wholesomemsg.pop(quoteno)
            #adding quotes and removing quotes. Quote number is auto adjusted to go from 0 to n-1

    if text in postingdict:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=postingdict.get(text))
#name based checking of posting, rarely used honestly
    if 'full nric' in processed:
        for admin in adminlist:
            cut = text[processed.find("rank"):]
            await context.bot.send_message(chat_id=admin, text=cut)
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Sent.')

#to forward messages about new sit inpro to us
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")



if __name__ == '__main__':
    # 6952678124:AAE0-r7FQjaPaMcmsrUmdGP9ZQ68LJ8bGaU
    application = ApplicationBuilder().token('6909497429:AAEhBZiIg6fqQ3nlLTWJmBDWreGNBcwW0bQ').build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    newsit_handler = CommandHandler('newsit', newsit)
    application.add_handler(newsit_handler)

    rules_handler = CommandHandler('rules', rules)
    application.add_handler(rules_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    sit_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), sit)
    application.add_handler(sit_handler)

    addposting_handler = CommandHandler('addposting', addposting)
    application.add_handler(addposting_handler)

    admin_handler = CommandHandler('admin', admin)
    application.add_handler(admin_handler)

    demote_handler = CommandHandler ('demote',demote)
    application.add_handler(demote_handler)

    deleteposting_handler = CommandHandler('deleteposting', deleteposting)
    application.add_handler(deleteposting_handler)

    viewposting_handler = CommandHandler('viewposting', viewposting)
    application.add_handler(viewposting_handler)

    wholesome_message_handler = CommandHandler('wholesome_message', wholesome_message)
    application.add_handler(wholesome_message_handler)

    reset_wholesome_message_handler = CommandHandler('reset_wholesome_message', reset_wholesome_message)
    application.add_handler(reset_wholesome_message_handler)


    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()


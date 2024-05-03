from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import filters, MessageHandler, ConversationHandler, ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext

users = [
        #{'ID': 1421339299, 'NAME': 'ASD', 'AGE': 'ASD', 'PHONE NUMBER': 'ASD', 'STATUS': 'ASD', 'ADMIN': False, 'FRAME': 'ASD', 'DATE OF COURSE END': 'ASD', 'DATE OF POSTING INTO SIT': 'ASD', 'NEXT OF KIN NAME': 'ASD', 'NEXT OF KIN RELATIONSHIP': 'ASD', 'NEXT OF KIN CONTACT': 'ASD', 'LICENSE NUMBER(IF ANY)': 'ASD', 'DRC (IF ANY)': 'ASD', 'POSTING': None, 'PARADE STATE': None},
        #{'ID': 1421339399, 'NAME': 'ASD', 'AGE': 'ASD', 'PHONE NUMBER': 'ASD', 'STATUS': 'ASD', 'ADMIN': False, 'FRAME': 'ASD', 'DATE OF COURSE END': 'ASD', 'DATE OF POSTING INTO SIT': 'ASD', 'NEXT OF KIN NAME': 'ASD', 'NEXT OF KIN RELATIONSHIP': 'ASD', 'NEXT OF KIN CONTACT': 'ASD', 'LICENSE NUMBER(IF ANY)': 'ASD', 'DRC (IF ANY)': 'ASD', 'POSTING': None, 'PARADE STATE': None},
        #{'ID': 1421339799, 'POSTING': "asdasdasd", 'PARADE STATE': None, 'NAME': 'A', 'PHONE NUMBER': 'SD', 'STATUS': 'AD', 'MASTER': False, 'ADMIN': False, 'FRAME': 'SA', 'DATE OF COURSE END': 'DAD', 'DATE OF POSTING INTO SIT': 'A', 'NEXT OF KIN NAME': 'DADA', 'NEXT OF KIN RELATIONSHIP': 'D', 'NEXT OF KIN CONTACT': 'A', 'LICENSE NUMBER(IF ANY)': 'DA', 'DRC (IF ANY)': 'DA'}
        ]
userKeyboard = [["UPDATE DETAILS", "VIEW POSTING"], ["UPDATE STATUS", "BOOK IN"]]
adminKeyboard = [["VIEW DETAILS", "PARADE STATE"], ["REMOVE POSTING", "ADD/EDIT POSTING"]]
masterKeyboard = [["MASTER VIEW", "CHANGE MSATER"], ["REMOVE ADMIN", "GIVE ADMIN"], ["CONTACT DEV", "ADD DATAS"]]

id_Posting = []
unit_Posting = []
vocation_Posting = []
date_Posting = []

async def userIndex():
    userIndex = {d["ID"]: i for i, d in enumerate(users)}
    return userIndex

async def userName():
    userName = {d["NAME"]: i for i, d in enumerate(users)}
    return userName


##############################################################################################
# Details 

async def userIndex():
    userIndex = {d["ID"]: i for i, d in enumerate(users)}
    return userIndex

async def updateDetails(Update: Update, Context: CallbackContext):
    Id = Update.effective_chat.id
    indexUsers = await userIndex()
    if (indexUsers.get(Id)) == None:
        users.append(
            {
                'ID': Update.effective_chat.id,
                'POSTING': None,
                'PARADE STATE': None
            }
        )
        await Update.message.reply_text('Welcome to SEMBAWANG SIT! LETS START UR REGISTRATION!')
    else:
        # EXTRA DETAILS
        index = indexUsers.get(Id)
        if (users[index]['POSTING']) != None:
            users[index]['POSTING'] = users[index]['POSTING']
        else:
            users[index]['POSTING'] = None

        if (users[index]['PARADE STATE']) != None:
            users[index]['PARADE STATE'] = users[index]['PARADE STATE']
        else:
            users[index]['PARADE STATE'] = None

    await Update.message.reply_text("RANK & NAME (FULL NAME AS PER NRIC): ")
    return 'NAME'

async def updateName(Update: Update, Context: CallbackContext):
    Id = Update.effective_chat.id
    # checks
    
    username = (Update.message.text).upper()
    indexUsers = await userIndex()
    index = indexUsers[Id]
    users[index]['NAME'] = username

    await Update.message.reply_text("AGE: ")
    return 'AGE'

async def updateAge(Update: Update, Context: CallbackContext):
    Id = Update.effective_chat.id
    # checks

    age = (Update.message.text).upper()
    indexUsers = await userIndex()
    index = indexUsers[Id]
    users[index]['NAME'] = age

    await Update.message.reply_text("PHONE NUMBER (IF U ARE USING A NON SINGAPORE NUMBER, ADD THE COUNTRY CODE IN FRONT.) \n\nEG. +65 12312312: ")
    return 'NUMBER'

async def updateNumber(Update: Update, Context: CallbackContext):
    Id = Update.effective_chat.id
    # checks

    number = (Update.message.text).upper()
    indexUsers = await userIndex()
    index = indexUsers[Id]
    users[index]['PHONE NUMBER'] = number

    await Update.message.reply_text("STATUS (COMPLETED COURSE/OOC/OOT): ")
    return 'STATUS'

async def updateStatus(Update: Update, Context: CallbackContext):
    Id = Update.effective_chat.id
    # checks
    status = (Update.message.text).upper()
    if status == 'ADMIN123456':
        indexUsers = await userIndex()
        index = indexUsers[Id]
        users[index]['ADMIN'] = True
        users[index]['MASTER'] = False

        print(users)
        await Update.message.reply_text(
            "ADMIN STARTED!!!",
            reply_markup=ReplyKeyboardMarkup(adminKeyboard, one_time_keyboard=True)
        )
        return 'COMMAND'
    elif status =='MASTERADMIN':
        masterExist = False
        for i in users:
            if i['ID'] == Update.effective_chat.id:
                continue
            else:
                if i['MASTER'] == True:
                    masterExist = True

        if masterExist== True:
            await Update.message.reply_text(
                'A MASTER ACCOUNT ALR EXIST. PLS CONTACT THE MASTER ACCOUNT TO CHANGE MASTERS.',
                reply_markup=ReplyKeyboardMarkup([['BACK TO START']], one_time_keyboard=True)
            )
            return 'BAIBAI'
        else:
            indexUsers = await userIndex()
            index = indexUsers[Id]
            users[index]['ADMIN'] = True
            users[index]['MASTER'] = True
            await Update.message.reply_text(
                "MASTER ADMIN STARTED!!!",
                reply_markup=ReplyKeyboardMarkup(masterKeyboard, one_time_keyboard=True)
            )
            return 'COMMAND'
    else:
        indexUsers = await userIndex()
        index = indexUsers[Id]
        users[index]['STATUS'] = status    
        users[index]['ADMIN'] = False
        users[index]['MASTER'] = False
        await Update.message.reply_text("FRAME (CLX FXXX): ")
        return 'FRAME'
    

async def updateFrame(Update: Update, Context: CallbackContext):
    Id = Update.effective_chat.id
    # checks

    Frame = (Update.message.text).upper()
    indexUsers = await userIndex()
    index = indexUsers[Id]
    users[index]['FRAME'] = Frame

    await Update.message.reply_text("DATE OF COURSE END (DDMMYYYY): ")
    return 'DATE OF COURSE END'

async def updateDCE(Update: Update, Context: CallbackContext):
    Id = Update.effective_chat.id
    # checks

    dce = (Update.message.text).upper()
    indexUsers = await userIndex()
    index = indexUsers[Id]
    users[index]['DATE OF COURSE END'] = dce

    await Update.message.reply_text("DATE OF POSTING INTO SIT (DDMMYYYY): ")
    return 'DATE OF POSTING INTO SIT'

async def updatePIS(Update: Update, Context: CallbackContext):
    Id = Update.effective_chat.id
    # checks

    pis = (Update.message.text).upper()
    indexUsers = await userIndex()
    index = indexUsers[Id]
    users[index]['DATE OF POSTING INTO SIT'] = pis

    await Update.message.reply_text("NEXT OF KIN NAME: ")
    return 'NEXT OF KIN NAME'

async def updateNOKN(Update: Update, Context: CallbackContext):
    Id = Update.effective_chat.id
    # checks

    nokn = (Update.message.text).upper()
    indexUsers = await userIndex()
    index = indexUsers[Id]
    users[index]['NEXT OF KIN NAME'] = nokn

    await Update.message.reply_text("NEXT OF KIN NAME: ")
    return 'NEXT OF KIN NAME'

async def updateNOKN(Update: Update, Context: CallbackContext):
    Id = Update.effective_chat.id
    # checks

    nokn = (Update.message.text).upper()
    indexUsers = await userIndex()
    index = indexUsers[Id]
    users[index]['NEXT OF KIN NAME'] = nokn

    await Update.message.reply_text("NEXT OF KIN RELATIONSHIP: ")
    return 'NEXT OF KIN RELATIONSHIP'

async def updateNOKR(Update: Update, Context: CallbackContext):
    Id = Update.effective_chat.id
    # checks

    nokr = (Update.message.text).upper()
    indexUsers = await userIndex()
    index = indexUsers[Id]
    users[index]['NEXT OF KIN RELATIONSHIP'] = nokr

    await Update.message.reply_text("NEXT OF KIN CONTACT: ")
    return 'NEXT OF KIN CONTACT'

async def updateNOKC(Update: Update, Context: CallbackContext):
    Id = Update.effective_chat.id
    # checks

    nokc = (Update.message.text).upper()
    indexUsers = await userIndex()
    index = indexUsers[Id]
    users[index]['NEXT OF KIN CONTACT'] = nokc

    await Update.message.reply_text("LICENSE NUMBER (IF ANY, CIVI): ")
    return 'LICENSE NUMBER (IF ANY)'

async def updateLicense(Update: Update, Context: CallbackContext):
    Id = Update.effective_chat.id
    # checks

    license = (Update.message.text).upper()
    indexUsers = await userIndex()
    index = indexUsers[Id]
    users[index]['LICENSE NUMBER(IF ANY)'] = license

    await Update.message.reply_text("DRC (IF ANY): ")
    return 'DRC (IF ANY)'

async def updateDRC(Update: Update, Context: CallbackContext):
    Id = Update.effective_chat.id
    # checks

    drc = (Update.message.text).upper()
    indexUsers = await userIndex()
    index = indexUsers[Id]
    users[index]['DRC (IF ANY)'] = drc

    # EXTRA DETAILS
    if (users[index]['POSTING']) != None:
        users[index]['POSTING'] = users[index]['POSTING']
    else:
        users[index]['POSTING'] = None

    if (users[index]['PARADE STATE']) != None:
        users[index]['PARADE STATE'] = users[index]['PARADE STATE']
    else:
        users[index]['PARADE STATE'] = None

    print(users)
    await Update.message.reply_text(
        "Registered!!!",
        reply_markup=ReplyKeyboardMarkup(userKeyboard, one_time_keyboard=True)
    )
    return 'COMMAND'


##############################################################################################
# VIEW POSTING

async def viewPosting(Update: Update, Context: CallbackContext):
    Id = Update.effective_chat.id
    indexUsers = await userIndex()
    index = indexUsers[Id]
    data = users[index]['POSTING']
    if (data) == None:
        data = "No posting for u yet...wait ba"
    else:
        data = data

    await Update.message.reply_text(
        text=data,
        reply_markup=ReplyKeyboardMarkup(userKeyboard, one_time_keyboard=True)
    )
    return 'COMMAND'

##############################################################################################
# VIEW DETAILS

async def viewDetails(Update: Update, Context: CallbackContext):
    for i in users:
        if (i['ADMIN']) == False:
            await Update.message.reply_text(
                f"ID: {i['ID']} \nNAME: {i['NAME']} \nAGE: {i['AGE']} \nPHONE NUMBER: {i['PHONE NUMBER']} \nSTATUS: {i['STATUS']} \nFRAME: {i['FRAME']} \nDATE OF COURSE END: {i['DATE OF COURSE END']} \nDATE OF POSTING INTO SIT: {i['DATE OF POSTING INTO SIT']} \nNEXT OF KIN NAME: {i['NEXT OF KIN NAME']} \nNEXT OF KIN RELATIONSHIP: {i['NEXT OF KIN RELATIONSHIP']} \nNEXT OF KIN CONTACT: {i['NEXT OF KIN CONTACT']} \nLICENSE NUMBER(IF ANY): {i['LICENSE NUMBER(IF ANY)']} \nDRC (IF ANY): {i['DRC (IF ANY)']} \nPOSTING: {i['POSTING']} \nPARADE STATE: {i['PARADE STATE']}",
            )
    
    await Update.message.reply_text(
        text="DONE",
        reply_markup=ReplyKeyboardMarkup(adminKeyboard, one_time_keyboard=True)
    )
    return 'COMMAND'


##############################################################################################
# ADD/EDIT POSTING

async def clearPosting():
    id_Posting.pop()
    unit_Posting.pop()
    vocation_Posting.pop()
    date_Posting.pop()

    return

async def namePosting(Update: Update, Context: CallbackContext):
    if len(id_Posting) > 0:
        await clearPosting()
    for i in users:
        if (i['ADMIN']) == False:
            await Update.message.reply_text(
                f"ID: {i['ID']} \nNAME: {i['NAME']} \nAGE: {i['AGE']} \nPHONE NUMBER: {i['PHONE NUMBER']} \nSTATUS: {i['STATUS']} \nFRAME: {i['FRAME']} \nDATE OF COURSE END: {i['DATE OF COURSE END']} \nDATE OF POSTING INTO SIT: {i['DATE OF POSTING INTO SIT']} \nNEXT OF KIN NAME: {i['NEXT OF KIN NAME']} \nNEXT OF KIN RELATIONSHIP: {i['NEXT OF KIN RELATIONSHIP']} \nNEXT OF KIN CONTACT: {i['NEXT OF KIN CONTACT']} \nLICENSE NUMBER(IF ANY): {i['LICENSE NUMBER(IF ANY)']} \nDRC (IF ANY): {i['DRC (IF ANY)']} \nPOSTING: {i['POSTING']} \nPARADE STATE: {i['PARADE STATE']}",
            )

    await Update.message.reply_text(
        'PLS ENSURE THAT ONLY 1 ADMIN IS EDITING THE DETAILS AT ANY TIME \n\nLAI LAI TELL ME THE ID OF THE PERSON U WAN EDIT POSTING FOR...'
    )
    return 'GETTING NAME FOR POSTING'

async def unitPosting(Update: Update, Context:CallbackContext):
    id_Posting.append(Update.message.text)
    await Update.message.reply_text('UNIT:')

    return 'GETTING UNIT FOR POSTING'    
    
async def vocationPosting(Update: Update, Context:CallbackContext):
    unit_Posting.append(Update.message.text)
    await Update.message.reply_text('VOCATION:')

    return 'GETTING VOCATION FOR POSTING'   

async def datePosting(Update: Update, Context:CallbackContext):
    vocation_Posting.append(Update.message.text)
    await Update.message.reply_text('DATE:')

    return 'GETTING DATE FOR POSTING'   
    
async def updatePosting(Update: Update, Context:CallbackContext):
    date_Posting.append(Update.message.text)
    indexUsers = await userIndex()
    index = indexUsers[int(id_Posting[0])]
    name = users[index]['NAME']
    details = f"\nNAME: {name} \nUNIT: {unit_Posting[0]} \nVOCATION: {vocation_Posting[0]} \nDATE: {date_Posting[0]}"
    users[index]['POSTING'] = details


    await Update.message.reply_text('POSTING HAS BEEN UPDATED')
    await Update.message.reply_text(
        details,
        reply_markup=ReplyKeyboardMarkup(adminKeyboard, one_time_keyboard=True)
    )
    
    return 'COMMAND'


##############################################################################################
# REMOVE POSTING

async def removePosting(Update: Update, Context: CallbackContext):
    for i in users:
        if (i['ADMIN']) == False:
            await Update.message.reply_text(
                f"ID: {i['ID']} \nNAME: {i['NAME']} \nAGE: {i['AGE']} \nPHONE NUMBER: {i['PHONE NUMBER']} \nSTATUS: {i['STATUS']} \nFRAME: {i['FRAME']} \nDATE OF COURSE END: {i['DATE OF COURSE END']} \nDATE OF POSTING INTO SIT: {i['DATE OF POSTING INTO SIT']} \nNEXT OF KIN NAME: {i['NEXT OF KIN NAME']} \nNEXT OF KIN RELATIONSHIP: {i['NEXT OF KIN RELATIONSHIP']} \nNEXT OF KIN CONTACT: {i['NEXT OF KIN CONTACT']} \nLICENSE NUMBER(IF ANY): {i['LICENSE NUMBER(IF ANY)']} \nDRC (IF ANY): {i['DRC (IF ANY)']} \nPOSTING: {i['POSTING']} \nPARADE STATE: {i['PARADE STATE']}",
            )

    await Update.message.reply_text(
        'PLS ENSURE THAT ONLY 1 ADMIN IS EDITING THE DETAILS AT ANY TIME \n\nLAI LAI TELL ME THE ID OF THE PERSON U WAN REMOVE POSTING FOR...'
    )
    return 'GETTING NAME FOR REMOVE'

async def updateRemove(Update: Update, Context: CallbackContext):
    indexUsers = await userIndex()
    Id = Update.message.text
    index = indexUsers[int(Id)]
    users[index]['POSTING'] = None

    await Update.message.reply_text(
        'POSTING HAS BEEN REMOVED',
        reply_markup=ReplyKeyboardMarkup(adminKeyboard, one_time_keyboard=True)
    )

    return 'COMMAND'


##############################################################################################
# UPDATE STATUS

async def getStatus(Update: Update, Context:CallbackContext):
    await Update.message.reply_text(
        'THIS FEATURE IS UNDER DEVELOPMENT \nPLS NEVER TRY IT AGAIN...TY',
        reply_markup=ReplyKeyboardMarkup(userKeyboard, one_time_keyboard=True)
    )

    return 'COMMAND'


##############################################################################################
# BOOK IN
    
async def bookIn(Update: Update, Context:CallbackContext):
    await Update.message.reply_text(
        'THIS FEATURE IS UNDER DEVELOPMENT \nPLS NEVER TRY IT AGAIN...TY',
        reply_markup=ReplyKeyboardMarkup(userKeyboard, one_time_keyboard=True)
    )    

    return 'COMMAND'

##############################################################################################
# PARADE STATE

async def paradeState(Update: Update, Context:CallbackContext):
    await Update.message.reply_text(
        'THIS FEATURE IS UNDER DEVELOPMENT \nPLS NEVER TRY IT AGAIN...TY',
        reply_markup=ReplyKeyboardMarkup(adminKeyboard, one_time_keyboard=True)
    )    

    return 'COMMAND'

##############################################################################################
# 



















##############################################################################################
# MASTER

async def masterView(Update: Update, Context: CallbackContext):
    for i in users:
        if ((i['MASTER']) == True) & ((i['ADMIN']) == True):
            await Update.message.reply_text('MEEE ^-^')
        await Update.message.reply_text(i)

    await Update.message.reply_text(
        'Done',
        reply_markup=ReplyKeyboardMarkup(masterKeyboard, one_time_keyboard=True)
    )

    return 'COMMAND'

async def giveAdmin(Update: Update, Context: CallbackContext):
    for i in users:
        if ((i['MASTER']) == True) & ((i['ADMIN']) == True):
            await Update.message.reply_text('MEEE ^-^')
        await Update.message.reply_text(i)

    await Update.message.reply_text(
        'WHOSE ADMIN RIGHTS DO U WAN TO EDIT (ID): '
    )

    return 'UPDATE GIVE ADMIN'

async def updateGiveAdmin(Update: Update, Context:CallbackContext):
    indexUsers = await userIndex()
    Id = Update.message.text
    index = indexUsers[int(Id)]
    users[index]['ADMIN'] = True

    await Update.message.reply_text(
        'ADMIN HAS BEEN GIVEN',
        reply_markup=ReplyKeyboardMarkup(masterKeyboard, one_time_keyboard=True)
    )

    return 'COMMAND'

async def removeAdmin(Update: Update, Context: CallbackContext):
    for i in users:
        if ((i['MASTER']) == True) & ((i['ADMIN']) == True):
            await Update.message.reply_text('MEEE ^-^')
        await Update.message.reply_text(i)

    await Update.message.reply_text(
        'WHOSE ADMIN RIGHTS DO U WAN TO EDIT (ID): '
    )

    return 'UPDATE REMOVE ADMIN'

async def updateRemoveAdmin(Update: Update, Context:CallbackContext):
    indexUsers = await userIndex()
    Id = Update.message.text
    index = indexUsers[int(Id)]
    users[index]['ADMIN'] = False

    await Update.message.reply_text(
        'ADMIN HAS BEEN REMOVED',
        reply_markup=ReplyKeyboardMarkup(masterKeyboard, one_time_keyboard=True)
    )

    return 'COMMAND'


async def changeMaster(Update: Update, Context: CallbackContext):
    for i in users:
        if ((i['MASTER']) == True) & ((i['ADMIN']) == True):
            await Update.message.reply_text('MEEE ^-^')
        await Update.message.reply_text(i)

    await Update.message.reply_text(
        'WHO DO U WAN TO BE MY MASTER ( ;-;) ID?: '
    )

    return 'UPDATE MASTER'

async def updateMaster(Update: Update, Context: CallbackContext):
    indexUsers = await userIndex()
    Id = Update.message.text
    index = indexUsers[int(Id)]
    users[index]['MASTER'] = True
    users[index]['ADMIN'] = True

    oldMaster = Update.effective_chat.id
    oldIndex = indexUsers[int(oldMaster)]
    users[oldIndex]['MASTER'] = False
    users[oldIndex]['ADMIN'] = False

    await Update.message.reply_text(
        'BAI BAI MASTER...',
        reply_markup=ReplyKeyboardMarkup([["BAI BAI"]], one_time_keyboard=True)
    )

    return 'BAIBAI'

async def contactDev(Update: Update, Context: CallbackContext):
    await Update.message.reply_text(
        'Should there be any bugs \nUpdates uall would like to add in OR if uall got ur own dev alr \nCONTACT ---> 88695889 \nEMAIL ---> kahjunt@gmail.com',
        reply_markup=ReplyKeyboardMarkup(masterKeyboard, one_time_keyboard=True)
    )

    return 'COMMAND'

async def addDatas(Update: Update, Context: CallbackContext):
    await Update.message.reply_text(
        'INPUT THE DICTIONARY: '
    )

    return 'UPDATE DATAS'

async def updateDatas(Update: Update, Context: CallbackContext):
    try:
        data_str = Update.message.text
        data = eval(data_str)  # Note: This assumes the user inputs a valid Python dictionary
    except Exception as e:
        print(f"Error parsing input as dictionary: {e}")
        await Update.message.reply_text('Invalid input. Please enter a valid dictionary.')
        return 'UPDATE DATAS'
    users.append(data)

    await Update.message.reply_text(
        'DATA ADDED TO USERS',
        reply_markup=ReplyKeyboardMarkup(masterKeyboard, one_time_keyboard=True)
    )

    return 'COMMAND'


##############################################################################################
# 




async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await Update.message.reply_text("Ended")

    return ConversationHandler.END


if __name__ == '__main__':
    # 6952678124:AAE0-r7FQjaPaMcmsrUmdGP9ZQ68LJ8bGaU actual
    # 6909497429:AAEhBZiIg6fqQ3nlLTWJmBDWreGNBcwW0bQ testing
    application = ApplicationBuilder().token('6909497429:AAEhBZiIg6fqQ3nlLTWJmBDWreGNBcwW0bQ').build()

    mainHandler = ConversationHandler(
        entry_points=[CommandHandler('start', updateDetails)],
        states={
            # MAINMENU
            # 'MENU': [MessageHandler(filters.TEXT & ~filters.COMMAND, defaultMenu)],
            'COMMAND': [
                # MASTER
                MessageHandler(filters.Regex("^MASTER VIEW$"), masterView),
                MessageHandler(filters.Regex("^CHANGE MASTER$"), changeMaster),
                MessageHandler(filters.Regex("^GIVE ADMIN$"), giveAdmin),
                MessageHandler(filters.Regex("^REMOVE ADMIN$"), removeAdmin),
                MessageHandler(filters.Regex("^CONTACT DEV$"), contactDev),
                MessageHandler(filters.Regex("^ADD DATAS$"), addDatas),
                # SITs
                MessageHandler(filters.Regex("^UPDATE DETAILS$"), updateDetails),
                MessageHandler(filters.Regex("^VIEW POSTING$"), viewPosting),
                MessageHandler(filters.Regex("^UPDATE STATUS$"), getStatus),
                MessageHandler(filters.Regex("^BOOK IN$"), bookIn),
                # ADMINs
                MessageHandler(filters.Regex("^VIEW DETAILS$"), viewDetails),
                MessageHandler(filters.Regex("^ADD/EDIT POSTING$"), namePosting),
                MessageHandler(filters.Regex("^REMOVE POSTING$"), removePosting),
                MessageHandler(filters.Regex("^PARADE STATE$"), paradeState),
            ],
            # Master
            'UPDATE MASTER': [MessageHandler(filters.TEXT & ~filters.COMMAND, changeMaster)],
            'UPDATE GIVE ADMIN': [MessageHandler(filters.TEXT & ~filters.COMMAND, updateGiveAdmin)],
            'UPDATE REMOVE ADMIN': [MessageHandler(filters.TEXT & ~filters.COMMAND, updateRemoveAdmin)],
            'UPDATE DATAS': [MessageHandler(filters.TEXT & ~filters.COMMAND, updateDatas)],
            'BAIBAI': [MessageHandler(filters.TEXT & ~filters.COMMAND, updateDetails)],

            # Add/Edit Postings
            'GETTING NAME FOR POSTING': [MessageHandler(filters.TEXT & ~filters.COMMAND, unitPosting)],
            'GETTING UNIT FOR POSTING': [MessageHandler(filters.TEXT & ~filters.COMMAND, vocationPosting)],
            'GETTING VOCATION FOR POSTING': [MessageHandler(filters.TEXT & ~filters.COMMAND, datePosting)],
            'GETTING DATE FOR POSTING': [MessageHandler(filters.TEXT & ~filters.COMMAND, updatePosting)],

            # Remove Postings
            'GETTING NAME FOR REMOVE': [MessageHandler(filters.TEXT & ~filters.COMMAND, updateRemove)],


            # Update Details
            'NAME': [MessageHandler(filters.TEXT & ~filters.COMMAND, updateName)],
            'AGE': [MessageHandler(filters.TEXT & ~filters.COMMAND, updateAge)],
            'NUMBER': [MessageHandler(filters.TEXT & ~filters.COMMAND, updateNumber)],
            'STATUS': [MessageHandler(filters.TEXT & ~filters.COMMAND, updateStatus)],
            'FRAME': [MessageHandler(filters.TEXT & ~filters.COMMAND, updateFrame)],
            'DATE OF COURSE END': [MessageHandler(filters.TEXT & ~filters.COMMAND, updateDCE)],
            'DATE OF POSTING INTO SIT': [MessageHandler(filters.TEXT & ~filters.COMMAND, updatePIS)],
            'NEXT OF KIN NAME': [MessageHandler(filters.TEXT & ~filters.COMMAND, updateNOKN)],
            'NEXT OF KIN RELATIONSHIP': [MessageHandler(filters.TEXT & ~filters.COMMAND, updateNOKR)],
            'NEXT OF KIN CONTACT': [MessageHandler(filters.TEXT & ~filters.COMMAND, updateNOKC)],
            'LICENSE NUMBER (IF ANY)': [MessageHandler(filters.TEXT & ~filters.COMMAND, updateLicense)],
            'DRC (IF ANY)': [MessageHandler(filters.TEXT & ~filters.COMMAND, updateDRC)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel)
        ]
    )
    application.add_handler(mainHandler)

    # newSIT = CommandHandler('Register', addUsers)
    # application.add_handler(newSIT)

    application.run_polling()

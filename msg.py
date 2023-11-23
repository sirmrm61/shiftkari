from enum import Enum


class messageLib(Enum):
    helloClient = 'سلام، {} \n به سرویس ارایه شیفت کاری خوش آمدی، من هیچ اطلاعاتی در مورد شما در بانک اطلاعاتیم ندارم اگر مایل به عضویت در این سرویس هستی با استفاده از کلیدهای زیر تعیین کن جزء چه گروهی هستی.'''
    enterName = 'نام خود را وارد نمائید'
    enterLastName = 'نام خانودگی خود را وارد نمائید'
    enterPhoneNumber = 'شماره تلفن همراه خود را وارد نمائید'
    enterPharmacyName = 'نام داروخانه را وارد نمائید'
    enterPharmacyType = 'نوع داروخانه را انتخاب نمائید'
    enterPharmacyAddress = 'آدرس داروخانه را وارد نمائید'
    enterPharmacyLicensePhoto = 'تصویر مجوز داروخانه را ارسال نمائید'
    endRegisteration = 'ثبت اطلاعات شما به پایان رسید اطلاعات شما برای تائید نهایی برای ادمین سیستم ارسال می شود تا زمان تائید ادمین شما اجازه فعالیت ندارید. باتشکر'
    errorSendFile = 'لطفا فایل عکس را ارسال نمائید'
    enterNationCode = 'شماره ملی خود را ارسال کنید'
    enetrcodePharmaceutical = 'شماره نظام داروسازی خود را وارد نمائید'
    enetrPhotoPharmaceutical = 'تصویر کارت عضویت نظام پزشکی خود را ارسال نمائید'
    enterLicenseStartDate = 'تاریخ شروع مجوز خود را ارسال نمائید\n فرمت تاریخ بدین صورت: 14000101'
    enterLicenseEndDate = 'تاریخ پایان مجوز خود را ارسال نمائید\n فرمت تاریخ بدین صورت: 14000101'
    enterWorkoverPermitPhoto = 'تصویر مجوز اضافه کار خود را ارسال نمائید'
    enterSelfiPhoto = 'عکس پرسنلی خود را ارسال نمائید'
    enterPermitActivity = 'شما در چه شیفتی مجاز به فعالیت هستید؟'
    enterVerifyOrDeny = 'با توجه به مدارک ارسال شده تائید یا عدم تائید کاربر را انجام دهید'
    helloAdmin = 'سلام {0}، شما بعنوان مدیر کانل وارد ربات شده اید و به امکانات ذیل دسترسی دارید';
    messAdminApproveStudent = 'دانشجویی با مشخصات ذیل ثبت نام کرده است مشخصات وی را بررسی سپس برای تائید و یا عدم تائید تصمیم بگیرد'
    labeName = 'نام و نام خانوادگی: {0} {1}'
    labelPhoneNumber = 'شماره تلفن: {0}'
    labelNationCode = 'شماره ملی: {0}'
    labelDateStartPermit = 'تاریخ شروع مجوز: {0}'
    labelDateEndPermit = 'تاریخ پایان مجوز: {0}'
    labelShift = 'شیفت مجاز: {0}'
    labelSelfiPhoto = 'عکس پرسنلی'
    labelPermitPhoto = 'عکس مجوز'
    messAdminApprove = 'آیا اطلاعات فوق را تائید می کنید'
    messAdminApproveFunder = 'موسسی با مشخصات ذیل ثبت نام کرده است مشخصات وی را بررسی سپس برای تائید و یا عدم تائید تصمیم بگیرید'
    labelPharmacyName = 'نام داروخانه: {}'
    labelPharmacyType = 'نوع داروخانه: {}'
    labelPharmacyAddress = 'آدرس داروخانه: {}'
    labelMembershipCardPhoto = 'تصویر کارت عضویت'
    messAdminApproveTechnical = 'یک مسئول فنی با مشخصات ذیل ثبت نام کرده است مشخصات وی را بررسی سپس برای تائید و یا عدم تائید تصمیم بگیرید'
    messAdminApproveAdmin = 'یک مدیر با مشخصات ذیل ثبت نام کرده است مشخصات وی را بررسی سپس برای تائید و یا عدم تائید تصمیم بگیرید'
    congratulationsApproveAdmin = 'تبریک عضویت شما توسط ادمین سیستم مورد تائید قرار گرفت'
    sorryDenyAdmin = 'متاسفانه اطلاعات شما به دلایل ذیل مورد تائید قرار نگرفت، پس از بررسی اطلاعات و رفع موانع می توانید دوباره ثبت نام نمائید'
    descDenyAdmin = 'لطفا دلیل عدم موافقت خود را ذکر نمائید'
    delMessageAdmin = 'اطلاعات کاربری ایشان حذف گردد'
    duplicateregistration = 'شما قبلا بعنوان {0}،در سیستم ثبت نام کرده اید آیا مایل به غیر فعال کردن نام کاربری  خود هستید؟\n در صورت انتخاب بلی شما اجازه فعالیت نخواهید داشت و شیفت ها برای شما ارسال نخواهد شد'
    myInfo = 'شما بعنوان {0}،با اطلاعات ذیل در سیستم ثبت نام کرده اید '
    afterDelete = 'نام کاربری شما در سامانه غیر فعال گردید برای فعالیت مجدد از دستور start استفاده کنید.'
    yourOperation = 'لیست فعالیت های شما؛کدام فعالیت را انتخاب می کنید؟'
    dateShift = 'لطفا تاریخ را وارد کنید(14020202)'
    notAccess = 'شما دسترسی ایجاد شیفت را ندارید.'
    shiftStartTime = 'ساعت شروع شیفت را وارد نمائید(16:00)'
    shiftEndTime = 'ساعت پایان شیفت را وارد نمائید(18:00)'
    shiftWage = 'میزان حق الزحمه هر ساعت را به ریال برای <b>مسئولان فنی</b> وارد نمائید'
    shiftWageStudent = 'میزان حق الزحمه هر ساعت را به ریال برای دانشجویان وارد نمائید'
    pharmacyAddress = 'آدرس داروخانه را وارنمائید'
    endRegisterShift = 'ثبت شیفت به پایان رسید اطلاعات شیفت برای مسئولان فنی و بعد از {0} ساعت در صورت نپذیرفتن توسط مسئولان فنی برای  دانشجویان ارسال خواهد شد.'
    emptyList = 'لیست مورد نظر شما خالی می باشد.'
    doYouLike = 'آیا تمایل به قبول این شیفت دارید؟'
    doYouLikeDelete = 'آیا تمایل به حذف این شیفت دارید؟'
    doYouLikeApprove = 'آیا تمایل به تائید این شیفت دارید؟'
    approvedByManager = 'درخواست شما جهت پیدا کردن جایگزین برای شیفت مورد تائید مدیر سیستم قرار گرفت و در لیست به همکاران نمایش داده خواهد شد.'
    disApprovedByManager = 'درخواست شما جهت پیدا کردن جایگزین برای شیفت مورد تائید مدیر سیستم قرار نگرفت.'
    delShiftMessage = 'این شیفت به صورت منطقی حذف گردید.'
    reserveShift = 'اطلاعات این شیفت برای شما رزرو شد. پس از تائید ارایه دهنده شیفت این شیفت برای شما قطعی می شود.'
    acceptShift = 'درخواست شما برای شیفت ذیل مورد پذیرش درخواست دهنده قرار گرفت'
    disAcceptShift = 'درخواست شما برای شیفت ذیل مورد پذیرش درخواست دهنده قرار نگرفت'
    invalidDate = 'تاریخ ورودی نامعتبر است'
    invalidTime = 'زمان ورودی نامعتبر است'
    youCanceled = 'شما شیفت تاریخ {0} را کنسل نمودید.'
    cancelShift = 'آقا/خانم {0} شیفت تاریخ {1} کنسل نموداند این تاریخ مجدد به دیگران جهت جایگزینی نمایش داده می شود.'
    oldDel = 'نام کاربری شما در سامانه غیر فعال شده است آیا مایل فعال کردن مجدد هستید؟'
    reActive = 'نام کاربری شما مجدد فعال گشت.'
    erroOnBack = 'شما یک مرحله بیشتر نمی توانید برگردید'
    diver = '-----------------------------'
    errorPhoneNumber = 'شماره تلفن همراهی  که وارد نموده اید معتبر نمی باشد. لطفا شماره صحیح را وارد نمائید.'
    errrorNation = 'کدملی که وارد کرده اید صحیح نمی باشد.کد ملی صحیح را وارد نمائید'
    shiftApprovedByManager = 'شیفتی که شما ساخته اید مورد تائید مدیر سیستم قرار گرفت'
    shiftDisApprovedByManager = 'شیفتی که شما ساخته اید مورد تائید مدیر سیستم قرار نگرفت'
    changeHour = '''زمان ارسال شیفت ها در صورت پر نشدن برای دانشجویان {0} ساعت بعد از ثبت شیفت است
    برا تغیر زماارسال شیفت ها از دستور ذیل استفاه کنید
/changeHrStudent 24'''
    changeWage = '''حداقل دستمزد برای شیفت ساعتی {0} ریال است 
    برا تغیر حداقل دستمزد از دستور زیر استفاده کنید
/changeMinWage 1200000'''
    changeLicenss = '''حداقل مبلغ اجاره پروانه {0} ریال است
    برا تغیر حداقل دستمزد پروانه از دستور زیر استفاده کنید
/changeMinLicenss 1200000'''
    erroCommand = ' فرمت دستوری که وارد کرده اید صحیح نمی باشد.'
    changeHourSuccess = ' زمان ارسال برای دانشجویان به {0} ساعت تغییر پیدا کرد'
    changeWageSuccess = 'حداقل دستمزد به {0} ریال تغییر پیدا کرد'
    changeLicenssSuccess = 'حداقل اجاره پروانه به {0} ریال تغییر پیدا کرد'
    repNationCode = 'کد ملی تکراریست'
    confirmDeleteShift = 'آیا از حذف کردن شیفت مطمئن هستید؟'
    enterDateEnd = 'تاریخ پایان شیفت را انتخاب کنید'
    hrPermitTotal = 'میزان ساعت فعالیت براساس مجوز را وارد نمائید'
    verifyMsg = 'شما اطلاعات کاربری {} تائید کردید.'
    editMessag = 'اطلاعات کاربری شما به شرح ذیل می باشد:\n'
    confirmEdit = 'اگر تمایل به ویرایش اطلاعات فوق دارید از کلید های زیر استفاده کنید.\n با عوض کردن هرکدام از اطلاعات کاربری شما تا تائید مجدد توسط ادمین غیر فعال خواهد شد.'
    errorTimeEdit = 'این درخواست بیش از 5 دقیقه پیش ارسال شده است.لطفا درخواست خود را دوباره ارسال کنید.'
    afterEdit = '''    مشخصه مورد نظر شما ویرایش شد، تاپس از تائید مدیر سیستم کاربر شما غیر فعال می گردد.
    آیا تمایل به ویرایش مشخصه دیگری دارید؟'''
    selectPropertyForEdit = 'یکی از مشخصه های زیر را برای ویرایش انتخاب کنید'
    sendAdminAfterEdit = 'کاربر فوق اطلاعاتش را ویرایش کرده است آیا اطلاعات موزد تائید است؟'
    sendToAdminMessage = 'اطلاعات شما برای مدیران سیستم ارسال گردید تا اطلاع بعدی فعالیت های شما محدود خواهد شد.'
    notVerifyAdmin = 'کاربری شما توسط مدیران سیستم تائید نشده است.'
    oldInfo = 'اطلاعات شما درسیستم به شرح ذیل می باشد'
    noShift =  'شیفتی برای پر کردن وجو ندارد'
    minWage = 'حداقل دستمزد برای شیفت برابر <b>{0}</b> است.'
    errorNumber = 'لطفا فقط عدد وارد نمائید.'
    doseVerify = 'تائید یا عدم تائید این کاربر قبلا توسط ادمین انجام شده است.'
    noBussiness = 'عملیات نا معتبر است.'
    shiftTotalDay = 'این شیف شامل {0} روز می باشد آیا تمام روز های شیفت را قبول می کنید؟'
    shiftSelectDay = 'از بین روز های ذیل روز مورد نظر خود را انتخاب نمائید'
    endShiftSelection = 'از لیست بالا روزهایی را که مایل هستید انتخاب نمائید. سپس کلید ذیل را بزنید تا انتخاب های شما برای تائید برای ایجاد کننده شیفت ارسال گردد.'
    afterDaySelction = 'شما تاریخ {0}انتخاب کردهاید برای ادامه انتخاب بر روی تاریخ دیگر کلیک کنید و گرنه پایان را انتخاب نمائید'
    repeatedDay = 'روز را تکراری انتخاب نموده اید.'
    shiftDayIsFull = 'این روز پر شده است'
    selectedDay = 'شما روز های زیر را انتخاب نموده اید، اگر مایل به حذف هرکدام از آنها می باشید رو آن کلیک نمائید در غیر اینصورت کلید تائید را کلیک نمائید.'
    emptSelectedDay = 'شما هیچ روزی را انتخاب نکرده اید.'
    sendForCreatorMessage = 'اگر از انتخاب ها مطمئن هستید کلید ارسال را کلیک نمائید.'
    sendDayForApproveCreator= ' آقا/خانم {0} درخواست پر کردن روزهای ذیل از شیفتی که ایجاد کرده اید را دارند، اطلاعات ایشان برای شما ارسال می گردد قبل تائید مطالعه بفرمائید'
    senndAcceptAllDayInShift = 'آقا/خانم {0} در خواست پرکردن کل روزهای شیفت را داده است اطلاعات ایشان برای شما ارسال میگردد قبل از تائید مطالعه بفرمائید'
    approvedDay = 'درخواست پرکردن شیفت برای تاریخ {0} از ایجاد کننده شیفت مورد پذیرش قرار گرفت'
    invalidApproveDate = 'این تاریخ را قبلا تائید کرده اید.'
    reqTitleMessageForCreator = 'فردی با مشخصات ذیل درخواست پرکردن شیفتی که شما ایجاد کرده اید را داده است'
    YourInfoToCreatorShift = ' درخواست شما برای سازنده شیفت ارسال گرید در صورت تائید به شما اطلاع رسانی می گردد'
    doYouLikeApproveRequest = 'آیا تمایل به پذیرش ذرخواست دارید؟'
    requesterNotify = 'به درخواست دهنده اطلاع رسانی انجام شد'
    msgSend = 'بعد از این پیام هر متنی ارسال کنید برای گروه انتخابی شما ارسال خواهد شد. اگر از ارسال پیام منصرف شدید از دستور زیر استفاده کنید \n /CancelMessage'
    cancelMsg = 'کاربری شما از حالت ارسال پیام خارج گردید'
    whoDoYouSend = 'برای چه گروهی می خواهسد پیام ارسال کنید؟'
    sendedMessage = 'پیامی ارسالی به گروه درخواستی ارسال گردید.'
    propertyShiftCreator = 'مشخصات ایجاد کننده شیفت.'
    minWFStudent = 'حداقل دستمزد دانشجو برای شیفت برابر {0} است.'
    wfStudenMessage = 'حداقل دستمز برای دانشجویان ساعتی {0} ریال میباشد اگر تمایل به تغییر آن دارید از دستور زیر استفاده نمائید.\n /changeWFS 10000'
    deleteMessage = '\n'+'آیا تمایل به حذف شیفت دارید؟'
    cancelShiftFromCreator = 'شیفتی که برای تاریخ {0} پذیرفته اید توسط سازنده شیفت کنسل شد.'
    shiftEMHrLabel = 'اگر فاصله زمانی تا شروع شیفت {0} ساعت باشد آن شیفت بعنوان شیفت اضطراری شناخت می شود.اگر مایلید این تعداد ساعت را عوض کنید از دستور زیر استفاده کنید'+\
                     '\n /changeShiftEmHr'
    pdLabel = 'شما در هر {0} روز میتوانید {1} شیفت اضطراری ارسال کنید.اگر تمایل دارید تعداروز را عوض کنید از دستور زیر استفاده کنید' +\
              '\n /changePDEM\n'+ 'اگر تمایل دارید تعداد شیفت را عوض کنید از دستور زیر استفاده کنید'+'\n /changeTPDEM'
    changeShiftEmHr = 'فاصله زمانی تشخیص شیفت اضطراری به {0} ساعت تغییر یافت'
    chandePDEM = 'تعداد روزهایی که شما می توانید در آن شیفت اضطراری تولید کنید به {0} روز تغیر کرد'
    chageTSPDEM = 'تعداد شیفت های اضطراری در بازه زمانی تعیین شده به {0} مرتبه تغییر پیدا کرد'
    emShiftMsg = 'تاریخی که شما ثبت نموده اید با توجه به قوانین ربات شیفت اضطراری می باشد سیستم در حال بررسی سوابق ارسال شیفت شما می باشد.' +\
                    'شما هر {0} روز قادرید {1} شیفت اضطراری ثبت کنید. شیفت اضطراری  پس از ثبت برای مسئولان فنی و دانشجویان همزمان ارسال می شود' +\
                 '\n'+'جهت ثبت شیفت اضطراری از عملیات من استفاده نمائید'
    emShiftFull = 'با توجه به اینکه شما تعداد شیفت های اضطراری مجاز خود را استفاده نموده اید امکان ثبت شیفت اضطراری نمی باشد.'
    emShiftRegister = 'شما درحال ثبت شیفت اضطراری می باشید.'
    registerEmShift = 'با توجه به زمان انتخابی شما باید شیف اضطراری ثبت کنید در غیر اینصورت زمان شروع شیفت را تغییر دهید.'
    emShiftMsgCreate = 'با توجه به قوانین سایت ' +\
                    'شما هر {0} روز قادرید {1} شیفت اضطراری ثبت کنید. شیفت اضطراری  پس از ثبت برای مسئولان فنی و دانشجویان همزمان ارسال می شود'
    endRegisterShiftEm = 'این شیفت بصورت همزمان برای دانشجو ها و مسئولان فنی ارسال گردید.'
    choiceDays = 'روزهای مورد نظر خود را انتخاب نمائید📆'
    choiceDaysMorning = 'تاریخ های مورد نظر خود را، برای شیفت صبح انتخاب نمائید({0})☀️️'
    choiceDaysEvening = 'تاریخ های مورد نظر خود را، برای شیفت عصر انتخاب نمائید({0})🌙'
    choiceDaysNight = 'تاریخ های مورد نظر خود را، برای شیفت شب انتخاب نمائید({0})🌃'
    licenseNeed = '✒️اطلاعات پروانه مورد نیاز خود را با جزئیات ثبت نمائید✒️'
    licenseEmpty = '✒️اطلاعات ساعات خالی پروانه خود را با جزئیات ثبت نمائید✒️'
    msgRegistedlicenseNeed = '📄شما یک آگهی نیاز به پروانه فعالییت با مشخصات فوق در سیستم ثبت کردید؛این آگهی به افرادی که آنرا جسجو کنند نمایش داده می شود.📄'
    msgRegistedlicenseEmpty = '📄شما یک آگهی پروانه با ساعات خالی ثبت نموده اید. این آگهی به افرادی که آنرا جستجو گنند نمایش داده می شود 📄'
    errorRegisterLicense ='🤷بت آپهس با خطا مواجه شد! بعدا دوباه سعی کنید.🤷‍'
    extensionLicensed = 'پیام مورد نظر با موفقیت تمدید گردید.'
    delLicensed = 'پیام مورد نظر با موفقیت حذف گردید.'
    searchMessage = 'دنبال چه چیزی می گردید؟'
    searchMessageFounder = 'بخشی از نام، نام خانوادگی، شماره همراه، نام داوخانه، نوع داروخانه و یا آدرس داروخانه را برای من ارسال کن.'
    searchMessageStudent = 'بخشی از نام، نام خانوادگی، شماره همراه،کد ملی، تاریخ شروع مجوز، تاریخ پایان مجوز ویا مجوز شیفت را برای من ارسال کن.'
    searchMessageTechnician = 'بخشی از نام، نام خانوادگی، شماره همراه و یا کد ملی را برای من ارسال کن.'
    searchMessageAdmin = 'بخشی از نام، نام خانوادگی و یا شماره همراه را برای من ارسال کن.'
    searchCancel = 'ربات از حالت جستجو خارج شد.'
    searchEmptyList = 'جسجوی شما نتیجه ایی در بر نداشت برای جستجوی مجدد کلمه مورد نظر را ارسال کن'
    promptChoseTypePharmacy = 'نوع داروخانه را انتخاب کنید.'
    promptStandardShift = '''
آیا در بازه های استاندارد ذیل شیفت می خواهید یا در زمان آزاد؟
صبح:{0}
عصر:{1}
شب:{2}
'''
    freeTimeMsg = 'برای تعیین زمان حضور در داروخانه بر روی تاریخ ها کلیک کنید.فرمت زمان (06->15)'
    enterTime = '''
زمان مورد نظر را برای تاریخ {0} وارد نمائید 
فرمت:ساعت ابتدایی-ساعت انتهایی
09:00-18:12
'''
    errorFormatTime = 'فرمت زمان ورودی صحیح نمی باشد لطفا مجدد سعی کنید.1401-17:03'
    errorConti = '  روز از این شیفت دارای زمان حضور در داروخانه نمی باشد لطفا زمان آنها را واردنمائید{0}'
    errorTotalDay ='شما تاریخی را انتخاب نکرده اید . آیا می خواهید از ثبت شیفت انصراف بدهید؟'
    cancelShiftMsg = 'شما ازادامه ثبت شیفت انصراف دادید هر زمانی می توانید ممجدد شیفت جدید ثبت کنید'
    shiftIsFull = 'روزهای این شیفت پر است.😢😢😢'
    noRegisterUser = '🥺🥺🥺شما ثبت نام نکرده اید 🥺🥺🥺'
    noForRegisterUser = 'برای ثبت نام از دستور زیر استفاده کن: \n /start'
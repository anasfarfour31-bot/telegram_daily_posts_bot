# Telegram Daily Posts Bot

يرسل منشورًا واحدًا يوميًا إلى قناة Telegram باستخدام GitHub Actions.

## الملفات

- `data/hikam.txt`: المنشورات، وكل منشور مفصول بسطر يحتوي على `---`
- `send_post.py`: سكربت الإرسال
- `.github/workflows/send_daily.yml`: تشغيل يومي تلقائي
- `state.json`: رقم المنشور القادم

## الإعداد

### 1. إنشاء بوت Telegram

1. افتح Telegram وابحث عن `@BotFather`
2. أرسل: `/newbot`
3. اختر اسمًا للبوت
4. انسخ الـ token الذي يعطيك إياه BotFather

### 2. إضافة البوت للقناة

1. افتح قناتك في Telegram
2. أضف البوت كـ Admin
3. أعطه صلاحية نشر الرسائل

### 3. معرفة Chat ID

إذا كانت القناة عامة، استخدم:
```
@YourChannelUsername
```

مثال:
```
@my_islamic_channel
```

إذا كانت القناة خاصة، تحتاج Chat ID يبدأ غالبًا بـ `-100`.
أسهل طريقة: اجعل القناة عامة مؤقتًا وضع username، أو استخدم بوتات معرفة الـ ID.

### 4. رفع الملفات إلى GitHub

1. أنشئ Repository جديد في GitHub
2. ارفع هذه الملفات كلها
3. يفضل أن يكون Public حتى تكون GitHub Actions مجانية على standard GitHub-hosted runners

### 5. إضافة Secrets

في GitHub:
`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

أضف:

```text
TELEGRAM_BOT_TOKEN
```

وقيمته token من BotFather.

ثم أضف:

```text
TELEGRAM_CHAT_ID
```

وقيمته مثل:

```text
@YourChannelUsername
```

### 6. تشغيل الاختبار

اذهب إلى:
`Actions` → `Send daily Telegram post` → `Run workflow`

إذا وصل المنشور للقناة، انتهى الإعداد.

## تغيير وقت النشر

افتح الملف:

```text
.github/workflows/send_daily.yml
```

وعدّل هذا السطر:

```yaml
- cron: "0 6 * * *"
```

GitHub يستخدم توقيت UTC.
مثال: تركيا UTC+3، لذلك `0 6 * * *` يعني الساعة 09:00 صباحًا بتوقيت تركيا.

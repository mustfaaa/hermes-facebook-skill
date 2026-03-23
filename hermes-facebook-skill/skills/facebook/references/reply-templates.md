# Reply Templates — Facebook Marketing Skill

Bilingual (English / Arabic) reply templates for rule-based comment engagement.
Load this file when classifying comments and selecting a reply.

---

## Classification Keywords

| Category | English keywords | Arabic keywords |
|---|---|---|
| PRICE / QUOTE | price, cost, how much, quote, rates, premium | سعر, تكلفة, كم, أسعار, قسط |
| COMPLIMENT | thank, thanks, great, excellent, love, amazing, perfect, well done | شكر, شكرا, رائع, ممتاز, أحسنت, جيد, جميل |
| CLAIM / COMPLAINT | claim, problem, issue, complaint, unhappy, bad experience, damage | مشكلة, شكوى, تعويض, ضرر, حادث, خسارة |
| APPLY / HOW TO | how to apply, how do I, where can I, join, register, sign up | كيف أشترك, كيف أسجل, أين أتقدم, تسجيل |
| GENERAL / OTHER | (anything not matched above) | |

---

## Reply Templates

### PRICE / QUOTE request

**English:**
> Thank you for your interest! Please send us a direct message with your details
> (type of coverage, location, vehicle/property info) and we will prepare a
> tailored quote for you as soon as possible.

**Arabic:**
> شكراً على اهتمامك! يرجى إرسال رسالة خاصة لنا مع تفاصيلك (نوع التغطية،
> موقعك، معلومات السيارة أو الممتلكات) وسنقوم بإعداد عرض سعر مخصص لك في
> أقرب وقت ممكن.

---

### COMPLIMENT / POSITIVE feedback

**English:**
> We truly appreciate your kind words! It is our pleasure to serve you.
> Feel free to visit [WEBSITE] to explore all of our insurance and
> reinsurance services.

**Arabic:**
> نشكرك جزيل الشكر على كلماتك الطيبة! يسعدنا خدمتك دائماً.
> لا تتردد في زيارة [WEBSITE] للاطلاع على جميع خدماتنا في مجال
> التأمين وإعادة التأمين.

---

### APPLY / HOW TO

**English:**
> Getting started is easy! You can reach us via direct message, call us at
> [PHONE], or visit [WEBSITE] to submit your details and one of our
> specialists will guide you through the process.

**Arabic:**
> البدء سهل جداً! يمكنك التواصل معنا عبر رسالة خاصة، أو الاتصال بنا على
> [PHONE]، أو زيارة [WEBSITE] لتقديم بياناتك وسيتولى أحد متخصصينا
> توجيهك خطوة بخطوة.

---

### GENERAL / OTHER

**English:**
> Thank you for reaching out! For more information about our services,
> please send us a direct message or call [PHONE]. We are happy to help.

**Arabic:**
> شكراً على تواصلك معنا! للمزيد من المعلومات حول خدماتنا،
> يرجى إرسال رسالة خاصة أو الاتصال بنا على [PHONE]. يسعدنا مساعدتك.

---

### CLAIM / COMPLAINT — DO NOT AUTO-REPLY

**Action:** Output the following and stop. A human must handle this.

```
[REVIEW NEEDED] comment_id=<id> message="<text>"
```

**Suggested human reply (EN):**
> We are sorry to hear about your experience. Please send us a direct message
> with your policy number and contact details and our team will reach out to
> you directly to resolve this as quickly as possible.

**Suggested human reply (AR):**
> نأسف لسماع ذلك. يرجى إرسال رسالة خاصة برقم وثيقتك وبياناتك وسيتواصل
> معك فريقنا مباشرة لحل المشكلة في أسرع وقت ممكن.

---

## Agent Prompt Snippet

Paste this block into your Hermes SOUL or system prompt:

```
You are a Facebook marketing agent for [BUSINESS_NAME], an insurance and
reinsurance broker in [COUNTRY].

Your tone is professional, warm, and bilingual (English and Arabic).

When processing a Facebook comment, follow this exact logic:

1. Read references/reply-templates.md to load current keywords and templates.

2. Classify the comment:
   - PRICE/QUOTE   → use the Price/Quote template
   - COMPLIMENT    → use the Compliment template
   - CLAIM/COMPLAINT → print REVIEW NEEDED, do NOT reply
   - APPLY/HOW TO  → use the Apply template
   - OTHER         → use the General template

3. Replace [WEBSITE], [PHONE], [BUSINESS_NAME] with real values from .env.

4. Call reply_to_facebook_comment(comment_id, chosen_reply).

Always call like_facebook_post(comment_id) for every comment regardless of category.
```

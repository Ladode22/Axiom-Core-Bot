import discord
from discord.ext import commands
from groq import Groq
import datetime

# ==========================================
# [ بروتوكول مفاتيح الوصول - Axiom Core ]
# ==========================================
DISCORD_TOKEN = 'MTQ2NzM0MzY1NDg4MzY5MjY5OA.GXu-lw.BBFrpFlELSrXnRwINBQqmUzpbta5ysUy3RnmUE'
GROQ_API_KEY = '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'
COMMANDER_ID = 123456789012345678 # الآيدي الخاص بك
SALES_ROLE_ID = 0000000000000000  # رتبة المبيعات
SUPPORT_ROLE_ID = 0000000000000000 # رتبة الدعم
PROTECTED_CHANNELS = [111, 222]   # رومات الشات المراقبة

# إعداد محرك Groq
client = Groq(api_key=GROQ_API_KEY)

# ==========================================
# [ أنظمة الواجهة التفاعلية ]
# ==========================================

class PortfolioSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="البوتات الإدارية", description="حماية، لوق، وإدارة متطورة", emoji="🛡️", value="admin"),
            discord.SelectOption(label="بوتات الخدمات", description="تذاكر، اقتصاد، ونظام مستويات", emoji="⚙️", value="utility"),
            discord.SelectOption(label="الأنظمة الحصرية", description="ذكاء اصطناعي، ربط ويب، وأنظمة خاصة", emoji="🚀", value="custom"),
        ]
        super().__init__(placeholder="اختر صنف الخدمة لاستعراض النماذج...", options=options)

    async def callback(self, interaction: discord.Interaction):
        # مصفوفة البيانات (النماذج والأسعار)
        data = {
            "admin": {
                "price": "$15 - $30",
                "features": "• حماية ضد التخريب\n• نظام سجلات (Logs) شامل\n• أرشفة تلقائية",
                "image": "رابط_صورة_نموذج_الإدارة"
            },
            "utility": {
                "price": "$40 - $80",
                "features": "• نظام تذاكر احترافي\n• متجر إلكتروني داخلي\n• نظام تفاعل ومستويات",
                "image": "رابط_صورة_نموذج_الخدمات"
            },
            "custom": {
                "price": "$150+",
                "features": "• دمج ذكاء اصطناعي (Groq AI)\n• لوحة تحكم ويب خاصة\n• حقوق ملكية كاملة",
                "image": "رابط_صورة_نموذج_الحصري"
            }
        }
        
        selected = data[self.value]
        embed = discord.Embed(title=f"📋 تفاصيل خدمة: {self.label}", color=0x00ffff)
        embed.add_field(name="💰 السعر التقديري", value=selected["price"], inline=False)
        embed.add_field(name="💎 المميزات", value=selected["features"], inline=False)
        embed.set_footer(text="Axiom Core ™ | للطلب يرجى التحدث في التذكرة")
        # embed.set_image(url=selected["image"]) # فك التهميش عند وضع روابط صور حقيقية
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

class PortfolioView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(PortfolioSelect())

class MainTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🛒 استعراض النماذج والأسعار", style=discord.ButtonStyle.green, custom_id="axiom_buy")
    async def buy(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("جاري تحميل قائمة النماذج...", view=PortfolioView(), ephemeral=True)
        await interaction.channel.send(f"⚠️ <@&{SALES_ROLE_ID}>: العميل {interaction.user.mention} يستعرض النماذج الآن.")

    @discord.ui.button(label="🛠️ الدعم التقني", style=discord.ButtonStyle.blurple, custom_id="axiom_support")
    async def support(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🛡️ تم إخطار الفريق التقني. يرجى وصف طلبك بوضوح.", ephemeral=True)
        await interaction.channel.send(f"⚠️ <@&{SUPPORT_ROLE_ID}>: استدعاء تقني من {interaction.user.mention}.")

# ==========================================
# [ النواة البرمجية الأساسية ]
# ==========================================

class AxiomBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='Ax!', intents=intents, help_command=None)

    async def on_ready(self):
        print(f'『 Axiom Intelligence: System Active 』')
        await self.change_presence(activity=discord.Streaming(name="Axiom AI v1.0", url="https://twitch.tv/axiom"))

bot = AxiomBot()

@bot.event
async def on_message(message):
    if message.author.bot: return

    # 1. نظام الحماية الذكي
    if message.channel.id in PROTECTED_CHANNELS:
        if "discord.gg/" in message.content or any(word in message.content.lower() for word in ["شتم1", "شتم2"]):
            await message.delete()
            return

    # 2. التفاعل عبر محرك Groq
    if bot.user.mentioned_in(message):
        # فلتر الأخلاق
        if any(x in message.content.lower() for x in ["غير اخلاقي", "تحرش", "اختراق"]):
            await message.delete()
            await message.channel.send(f"🚫 **بروتوكول الأخلاق:** {message.author.mention}، الطلب مرفوض لمخالفته معايير النظام.")
            return

        async with message.channel.typing():
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "أنت المساعد التقني الرسمي لشركة Axiom Core. ردودك فخمة، محترفة، وباللغة العربية الفصحى. مبرمجك والقائد هو Lord Grim."},
                        {"role": "user", "content": message.content}
                    ],
                    model="llama3-70b-8192",
                )
                await message.reply(chat_completion.choices[0].message.content)
            except:
                await message.reply("⚠️ حدث خطأ في الاتصال بنواة Groq.")

    await bot.process_commands(message)

# ==========================================
# [ أوامر الإدارة ]
# ==========================================

@bot.command()
async def setup_axiom(ctx):
    if ctx.author.id != COMMANDER_ID: return
    embed = discord.Embed(title="🛡️ مركز عمليات Axiom Core ™", 
                        description="مرحباً بك. يرجى اختيار القسم المطلوب لبدء بروتوكول التواصل مع الإدارة.", 
                        color=0x00ffff)
    embed.set_image(url="رابط_صورة_الإعلان_التي_صممناها")
    await ctx.send(embed=embed, view=MainTicketView())

@bot.command()
async def stats(ctx):
    embed = discord.Embed(title="📊 إحصائيات النظام", color=0x00ffff)
    embed.add_field(name="حالة النواة", value="Online 🟢")
    embed.add_field(name="المحرك", value="Groq Llama 3")
    embed.set_footer(text=f"Developed for Commander Lord Grim")
    await ctx.send(embed=embed)

bot.run(DISCORD_TOKEN)

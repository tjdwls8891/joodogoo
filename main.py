# 라이브러리 임포트
import discord
import arrow
import random
import os
import time

# 봇 클라이언트 정의
bot = discord.Client()

# 상태메시지에 들어가는 문자열
bot_game = '출석체크'

# 봇 절대경로
path = 'C:\\Users\\i6680\\PycharmProjects\\joodogoo\\'

# 서버 시작 명령어 활성화 여부
server_start = False


# 날짜 문자열 만드는 함수
def today():
    day_of_the_week = '월화수목금토일'[arrow.now().weekday()]
    date = str(arrow.now().date())[5:].split('-')
    result = '%s월 %s일 %s요일' % (date[0], date[1], day_of_the_week)

    return result


# 계정 생성 시각 문자열
def client_created_at(text):
    date_time = text.split(' ')
    date = date_time[0].split('-')
    time = date_time[1].split(':')
    time[2] = time[2].split('.')[0]
    date_result = '%s년 %s월 %s일\n' % (date[0], date[1], date[2])

    if int(time[0]) > 12:
        am_or_pm = ' 오후 '
        time[0] = str(int(time[0]) - 12)
    else:
        am_or_pm = ' 오전 '
        if int(time[0]) < 10:
            time[0] = time[0][1]

    time_result = '%s시 %s분 %s초' % (time[0], time[1], time[2])
    result = date_result + am_or_pm + time_result

    return result


# 봇 켤 때 호출
@bot.event
async def on_ready():
    print('bot ready.\nBot code : joodogoo')  # 봇 준비 시 메시지
    game = discord.Game(bot_game)
    await bot.change_presence(status=discord.Status.online, activity=game)  # 상태 온라인 설정, 상태 메시지 설정


# 메시지를 받을 때 호출
@bot.event
async def on_message(message):
    global msg
    if message.content.startswith('!출석'):
        msg = await message.channel.send('@everyone 출석하세요!')  # 맨션으로 모든 사람에게 알림 보내기

        global ID, attendance
        ID = msg.id  # 출석 메시지인지 판별하기 위한 변수
        attendance = []  # 출석자 명단 초기화

        await msg.add_reaction('✅')  # 출석 반응용 이모지 추가

    if message.content.startswith('!공지'):
        content = message.content[4:]  # 명령어 부분 제거

        embed = discord.Embed(title='공지사항', description='@everyone ' + content, color=0xdddddd)  # 임베드 제목, 내용, 색 설정
        embed.set_footer(icon_url=message.author.avatar_url,
                         text=message.author.name + '#' + message.author.discriminator + ' ------- ' + today())  # 아래 공지한 사람, 날짜 표시

        await message.channel.send('@everyone', embed=embed)  # 임배드 안의 맨션은 알림 효과가 없으므로 밖에서도 맨션

    if message.content.startswith('!프로필'):
        if os.path.isfile(path + 'info_body\\{0}.txt'.format(str(message.author.id))):
            txt_i = open(path + 'info_body\\{0}.txt'.format(str(message.author.id)), 'r')
            info_v = txt_i.read()
            height, weight = info_v.split('$')
            txt_i.close()
        else:
            height = str(random.randrange(5, 25))
            weight = str(random.randrange(30, 120))
        embed = discord.Embed(title=message.author.display_name + '님의 프로필', color=0xdddddd)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.add_field(name='신장 - 체중', value=height + 'cm - ' + weight + 'g', inline=False)
        if os.path.isfile(path + 'info_field\\{0}.txt'.format(str(message.author.id))):
            txt = open(path + 'info_field\\{0}.txt'.format(str(message.author.id)))
            msg = txt.read()
            msg_list = msg.split('][')
            for i in msg_list:
                embed.add_field(name=i.split('$')[0], value=i.split('$')[1])
        embed.add_field(name='가입 날짜', value=client_created_at(str(message.author.created_at)), inline=False)
        if message.content == '!프로필 날짜제거':
            embed.set_footer(icon_url=message.author.avatar_url,
                             text=message.author.name + '#' + message.author.discriminator)
        else:
            embed.set_footer(icon_url=message.author.avatar_url,
                             text=message.author.name + '#' + message.author.discriminator + ' ------- ' + today())
        await message.channel.send(embed=embed)

    if message.content.startswith('!등록'):
        msg = message.content.split()

        if msg[1] == "필드":
            field_name = msg[2]
            field_txt = msg[3]
            user_id_txt = path + 'info_field\\{0}.txt'.format(str(message.author.id))
            if os.path.isfile(user_id_txt):
                txt = open(user_id_txt, 'a')
                txt.write('][' + field_name + '$' + field_txt)
                txt.close()
                await message.channel.send('등록되었습니다!')
            else:
                txt = open(user_id_txt, 'w')
                txt.write(field_name + '$' + field_txt)
                txt.close()
                await message.channel.send('등록되었습니다!')

        elif msg[1] == "신체":
            num_k = int(msg[2])
            num_m = int(msg[3])
            if num_k < 5 or num_k > 25:
                await message.channel.send('키는 5와 25 사이의 숫자만 입력 가능합니다!')
            elif num_m < 20 or num_m > 180:
                await message.channel.send('몸무게는 20와 180 사이의 숫자만 입력 가능합니다!')
            else:
                user_id_txt = path + 'info_body\\{0}.txt'.format(str(message.author.id))
                txt = open(user_id_txt, 'w')
                result = str(num_k) + '$' + str(num_m)
                txt.write(result)
                txt.close()
                await message.channel.send('키 %scm, 몸무게 %sg로 등록되었습니다.' % (num_k, num_m))

        elif msg[1] == "줌":
            zoom_name = msg[2]
            zoom_link = msg[3]
            user_id_txt = path + 'info_zoom\\{0}.txt'.format(str(message.author.id))
            if os.path.isfile(user_id_txt):
                txt = open(user_id_txt, 'a')
                txt.write('][' + zoom_name + '()()' + zoom_link)
                txt.close()
                await message.channel.send('등록되었습니다!')
            else:
                txt = open(user_id_txt, 'w')
                txt.write(zoom_name + '()()' + zoom_link)
                txt.close()
                await message.channel.send('등록되었습니다!')

    if message.content.startswith("!줌"):
        if os.path.isfile(path + 'info_zoom\\{0}.txt'.format(str(message.author.id))):
            txt = open(path + 'info_zoom\\{0}.txt'.format(str(message.author.id)))
            msg = txt.read()
            msg_list = msg.split('][')
            embed = discord.Embed(title='줌 링크', color=0xdddddd)

            for i in msg_list:
                link = "[링크](%s)" % i.split('()()')[1]
                embed.add_field(name=i.split('()()')[0], value=link)
            await message.channel.send(embed=embed)

    if message.content.startswith("!서버 시작") and message.author.guild_permissions.administrator:
        msg = await message.channel.send("제가 가진 권한을 확인합니다...")
        if msg.author.guild_permissions.administrator:
            time.sleep(2)
            await msg.edit(content="인증에 성공했습니다.")
            time.sleep(3)
            await msg.edit(content="현재 서버에 생성된 모든 채널을 삭제하고 재구성합니다.\n'서버 재구성 동의' 를 입력하여 동의하세요.\n*이 과정에서 삭제한 채널은 복구할 수 없습니다. 신중히 선택하세요.*")
            global server_start
            server_start = True
        else:
            time.sleep(2)
            await msg.edit(content="인증에 실패했습니다.")
            time.sleep(3)
            await msg.edit(content="이 기능을 사용하려면 관리자 권한이 필요합니다.\n봇에게 관리자 권한을 부여해주세요.")

    if message.content == "서버 재구성 동의" and server_start and message.author.guild_permissions.administrator:
        server_start = False
        await message.add_reaction('✅')
        await msg.edit(content="동의 확인되었습니다!")
        time.sleep(3)
        await message.delete()
        await msg.edit(content="서버 채널을 모두 삭제하고 안내 채널을 생성합니다.")
        time.sleep(4)
        for i in message.guild.text_channels:
            await i.delete()
        for i in message.guild.voice_channels:
            await i.delete()
        for i in message.guild.categories:
            await i.delete()
        chn = await message.guild.create_text_channel('안내_채널')
        msg = await chn.send("안내 채널이 생성되었습니다.")
        time.sleep(3)
        await msg.edit(content="카테고리를 생성중입니다...")
        time.sleep(1)
        cat_s = await message.guild.create_category(name="시스템")
        cat_o = await message.guild.create_category(name="명령어")
        cat_c = await message.guild.create_category(name="채팅")
        cat_ca = await message.guild.create_category(name="통화")
        await msg.edit(content="채팅 채널을 생성중입니다...")
        time.sleep(1)
        await message.guild.create_text_channel(name="공지", category=cat_s)
        await message.guild.create_text_channel(name="봇_명령어", category=cat_o)
        await message.guild.create_text_channel(name="채팅방", category=cat_c)
        await message.guild.create_text_channel(name="사진_게시판", category=cat_c)
        await msg.edit(content="음성 채널을 생성중입니다...")
        time.sleep(1)
        await message.guild.create_voice_channel(name="통화방 1호", category=cat_ca)
        await message.guild.create_voice_channel(name="통화방 2호", category=cat_ca)
        await message.guild.create_voice_channel(name="통화방 3호", category=cat_ca)
        time.sleep(2)
        await msg.edit(content="서버 구성이 완료되었습니다.")
        time.sleep(2)
        await msg.edit(content="안내 채널을 삭제합니다.")
        time.sleep(2)
        await msg.channel.delete()


# 리액션이 추가되었을 때 호출
@bot.event
async def on_reaction_add(reaction, user):
    global ID
    global msg
    if reaction.message.id == ID:  # 출석 명령어 메시지에 추가된 반응인지 확인
        if not attendance:  # 명단이 빈 경우. 주도구 봇이 반응을 처음 추가할 때 호출

            attendance.append(user.name)  # 리스트에 값을 추가해서 다시 실행되지 않도록

            embed = discord.Embed(title='출석자 명단', description='@everyone Hello!', color=0xdddddd)
            embed.set_footer(text='떠든사람 : 주도구' + ' ------- ' + today())

            msg = await reaction.message.channel.send(embed=embed)  # 보낸 메시지를 후에 수정하기 위해 전역변수에 저장

        elif attendance.count(user.name) == 0:  # 중복 출석 방지

            attendance.append(user.name)  # 출석자 명단 리스트에 추가

            embed = discord.Embed(title='출석자 명단', description='@everyone Hello!', color=0xdddddd)
            embed.set_footer(text='떠든사람 : 주도구' + ' ------- ' + today())
            for i in attendance[1:]:  # 처음 추가한 주도구 프로필을 제외하고 임베드 필드에 추가
                embed.add_field(name=i, value='출석 완료')

            await msg.edit(embed=embed)  # 출석자 명단 메시지를 수정. 알림이 여러 번 가지 않도록 맨션 생략


# 콧 토큰
bot.run('토큰')
# 다른 봇 초대코드 정리 혹으 ㄴ자동 초대, 봇이나 역할 관리, 서버 구성 커스텀

import nextcord
import re
import math


async def asmd(ctx, split, value):
    regex = re.compile('[@_!#\'\"$%^&\+*\-()<>\\\?/\|}{~:]')
    if value == '+':
        sum = 0.0
        small = 'ADD'
        big = 'addition'
    elif value == '-':
        small = 'SUBTRACT'
        big = 'subtraction'
    elif value == '*':
        sum = 1
        small = 'MULTIPLY'
        big = 'multiplication'
    elif value == '/':
        small = 'DIVIDE'
        big = 'division'
    first_loop = True
    for i in split:
        if i == '':
            continue
        for j in i:
            if j.isalpha():
                await ctx.send(embed=nextcord.Embed(title=f"When I saw the '{j}' in your message",
                                                    description=f"I realised the bitter truth.\nPeople don't see that REALITY DOESN'T ALLOW YOU TO {small} ALPHABETS!",
                                                    color=nextcord.Color.random()))
                return None
        if regex.search(i) is not None:
            if regex.search(i).group() == '+':
                if regex.search(i).span() != (0, 1):
                    await ctx.send(embed=nextcord.Embed(title=f"Remember this.",
                                                        description=f"You need to put the + sign before a number if you want to use it.",
                                                        color=nextcord.Color.random()))
                    return None
            elif regex.search(i).group() == '-':
                if regex.search(i).span() != (0, 1):
                    await ctx.send(embed=nextcord.Embed(title=f"Remember this also.",
                                                        description=f"You need to put the - sign before a number if you want to use it.",
                                                        color=nextcord.Color.random()))
                    return None
            elif regex.search(i).group() == '*':
                if value != '*':
                    await ctx.send(embed=nextcord.Embed(title=f"No multiplication in {big}.",
                                                        description=f"One of the basic laws of phys-, I mean, Mathematics",
                                                        color=nextcord.Color.random()))
                else:
                    await ctx.send(embed=nextcord.Embed(title=f"Ik this is {big}",
                                                        description=f"But honestly, '*' is not required here."))
            elif regex.search(i).group() == '/':
                if value != '/':
                    await ctx.send(embed=nextcord.Embed(title=f"No division in {big}.",
                                                        description=f"One of the basic laws of chem-, I mean, Mathematics\nDang it!",
                                                        color=nextcord.Color.random()))
                else:
                    await ctx.send(embed=nextcord.Embed(title=f"Ik this is {big}",
                                                        description=f"But honestly, '/' is not required here."))
            elif regex.search(i).group() == '=':
                await ctx.send(embed=nextcord.Embed(title=f"The = sign is a vital part of Maths",
                                                    description=f"But do you really think its required here?",
                                                    color=nextcord.Color.random()))
            else:
                await ctx.send(
                    embed=nextcord.Embed(
                        title=f"Why do you think that putting '{regex.search(i).group()}' is a good idea.",
                        description=f"Please guys, {big} isn't that complex!",
                        color=nextcord.Color.random()))

        if value == '+':
            sum = sum + float(i)
            if sum.is_integer() is True and not ('e' in str(sum)):
                sum = int(sum)
        elif value == '-':
            if first_loop is True:
                sum = float(i)
                first_loop = False
            else:
                sum = sum - float(i)
                if sum.is_integer() is True and not ('e' in str(sum)):
                    sum = int(sum)
        elif value == '*':
            sum = sum * float(i)
            if sum.is_integer() is True and not ('e' in str(sum)):
                sum = int(sum)
        elif value == '/':
            if first_loop is True:
                sum = float(i)
                first_loop = False
            else:
                sum = sum / float(i)
                if sum.is_integer() is True and not ('e' in str(sum)):
                    sum = int(sum)
    return sum


async def power_funcs(ctx, number, power, power_or_root):
    for i in power:
        if not i.isdigit():
            await ctx.send(embed=nextcord.Embed(title="I don't accept any alphabets or special signs yet.",
                                                description="My devs are trying to teach me about negative powers, but honestly I'm busy helping you guys :)",
                                                color=nextcord.Color.random()))
            return None
    first_loop = True
    for i in number:
        if not i.isdigit() or i == '+' or i == '-':
            if first_loop is True:
                first_loop = False
                if i == '-' and power_or_root == "root":
                    if float(power) % 2 == 1:
                        continue
                    else:
                        await ctx.send(embed=nextcord.Embed(title="Even powers don't have negative roots.",
                                                            color=nextcord.Color.random()))
                        return None
                else:
                    if i == '+' or i == '-' or i == '.':
                        pass
                    else:
                        await ctx.send(embed=nextcord.Embed(title=f"Oof that's sad",
                                                            description=f"You can't use '{i}' like that",
                                                            color=nextcord.Color.random()))
                        return None

            else:
                if i == '.':
                    continue
                else:
                    await ctx.send(embed=nextcord.Embed(title=f"This is UNACCEPTABLE",
                                                        description=f"This function OBVIOUSLY does not allow alphabets and special characters.\n'{i}' comes under that category.",
                                                        color=nextcord.Color.random()))
                    return None

    if power_or_root == "power":
        try:
            ans = round(math.pow(float(number), float(power)), 3)
        except OverflowError:
            embed = nextcord.Embed(title=f"The answer is TOO BIG",
                                   description=f"Its very size will demolish your sense of comprehension.\nOn looking at the answer, your two brain cells will short circuit and everything and everyone you love...\nwill be gone",
                                   color=nextcord.Color.random())
            embed.set_footer(text="So imma safely say that you don't wanna know")
            await ctx.send(embed=embed)
            return None
    elif power_or_root == "root":
        if '-' in str(number):
            ans = -(round(math.pow(abs(float(number)), 1 / float(power)), 3))
        else:
            ans = round(math.pow(float(number), 1 / float(power)), 3)
    if ans.is_integer() is True and not ('e' in str(ans)):
        return int(ans)
    return ans

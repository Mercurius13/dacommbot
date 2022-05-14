from time import time
from nextcord.ext import commands
from inspect import getsource
import nextcord
import os
import sys


class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def resolve_variable(self, variable):
        if hasattr(variable, "__iter__"):
            var_length = len(list(variable))
            if (var_length > 100) and (not isinstance(variable, str)):
                return f"<a {type(variable).__name__} iterable with more than 100 values ({var_length})>"
            elif not var_length:
                return f"<an empty {type(variable).__name__} iterable>"

        if (not variable) and (not isinstance(variable, bool)):
            return f"<an empty {type(variable).__name__} object>"
        return (variable if (
                    len(f"{variable}") <= 1000) else f"<a long {type(variable).__name__} object with the length of {len(f'{variable}'):,}>")

    def prepare(self, string):
        arr = string.strip("```").replace("py\n", "").replace("python\n", "").split("\n")
        if not arr[::-1][0].replace(" ", "").startswith("return"):
            arr[len(arr) - 1] = "return " + arr[::-1][0]
        return "".join(f"\n\t{i}" for i in arr)

    @commands.command(pass_context=True, aliases=['eva', 'exec', 'evaluate'])
    async def eval(self, ctx, *, code: str):
        if ctx.message.author.id == 815555652780294175 or 723032217504186389:
            silent = ("-s" in code)

            code = self.prepare(code.replace("-s", ""))
            args = {
                "discord": nextcord,
                "sauce": getsource,
                "sys": sys,
                "os": os,
                "imp": __import__,
                "this": self,
                "ctx": ctx
            }

            try:
                exec(f"async def func():{code}", args)
                a = time()
                response = await eval("func()", args)
                if silent or (response is None) or isinstance(response, nextcord.Message):
                    del args, code
                    return

                await ctx.send(
                    f"```py\n{self.resolve_variable(response)}````{type(response).__name__} | {(time() - a) / 1000} ms`")
            except Exception as e:
                await ctx.send(f"Error occurred:```\n{type(e).__name__}: {str(e)}```")

            del args, code, silent
        else:
            e = nextcord.Embed(title=":warning: IMPOSTER Detected :warning:",
                              description="You don't have the permissions to use this command!",
                              color=nextcord.Color.red())
            await ctx.send(embed=e)
            return


def setup(bot):
    bot.add_cog(Eval(bot))

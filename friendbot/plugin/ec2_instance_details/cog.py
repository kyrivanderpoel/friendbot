import attr
import discord
from discord.ext import commands

from ...cog import ClassLoggingCog
from ...util import bold
from .util import is_running_on_ec2, get_local_host_name, EC2InstanceMetaDataCollector


@attr.s
class EC2InstanceDetails(ClassLoggingCog):
    @commands.command(name="ec2-instance-details", help="prints whatever text you provide back")
    async def ec2_instance_details(self, ctx):
        """Returns the args back to the user."""
        self.logger.info(is_running_on_ec2())
        if is_running_on_ec2():
            data = EC2InstanceMetaDataCollector()
            message = f"""
{ctx.author.mention} here are the details about the EC2 instance running friendbot:

{bold('Instance ID:')} {data.instance_id}
{bold('AMI ID:')}      {data.ami_id}
{bold('Hostname:')}    {data.hostname}
"""
        else:

            message = f"""
{ctx.author.mention} this is not an EC2 instance. It is likely a testing environment:

{bold('Hostname:')} {get_local_host_name()}
"""
        embed = discord.Embed(description=message)
        await ctx.send(embed=embed)



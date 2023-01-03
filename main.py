import discord

intents = discord.Intents().all()
client = discord.Client(command_prefix=',', intents=intents)

# Ajout d'un role 
async def add_role(message, user, role):
    # Regarde si l'user a deja le role
    if role in user.roles:
        return f'{user.mention} already has the {role} role.'
    # Vérifie les permissions
    elif message.author.guild_permissions.manage_roles:
        await user.add_roles(role)
        return f'{user.mention} has been given the {role} role.'
    else:
        return f'{message.author.mention} does not have permission to manage roles.'

# Suppression du rôle d'un utilisateur
async def remove_role(message, user, role):
    # Regarde si l'user a le role
    if role in user.roles:
        # Vérifie les permissions
        if message.author.guild_permissions.manage_roles:
            await user.remove_roles(role)
            return f'The {role} role has been removed from {user.mention}.'
        else:
            return f'{message.author.mention} does not have permission to manage roles.'
    else:
        return f'{user.mention} does not have the {role} role.'


# Creation d'un role
async def create_role(message, role_name, permissions):
    # Vérifie les permissions
    if message.author.guild_permissions.manage_roles:
        # Creation
        new_role = await message.guild.create_role(name=role_name, permissions=permissions)
        return f'The {new_role} role has been created.'
    else:
        return f'{message.author.mention} does not have permission to manage roles.'


# Suppression d'un role
async def delete_role(message, role):
    # Vérifie les permissions
    if message.author.guild_permissions.manage_roles:
        # Supprime
        await role.delete()
        return f'The {role} role has been deleted.'
    else:
        return f'{message.author.mention} does not have permission to manage roles.'

# Liste les roles
async def list_roles(message):
    role_list = message.guild.roles
    role_names = []
    for role in role_list:
        role_names.append(role.name)
    return '\n'.join(role_names)

# Liste les rôles d'un utilisateur
async def list_user_roles(message, user):
    role_list = user.roles
    role_names = []
    for role in role_list:
        role_names.append(role.name)
    return '\n'.join(role_names)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Divise le message en commande et arguments
    parts = message.content.split(' ')
    command = parts[0][1:].lower()
    args = parts[1:]

    # syntaxe des commandes
    if command == 'addrole':
        if len(args) < 2:
            return 'Please specify a user and role to add.'
        # Prend l'user et le role
        user = discord.utils.get(message.guild.members, mention=args[0])
        if user is None:
            return 'That user does not exist.'
        role = discord.utils.get(message.guild.roles, name=args[1])
        if role is None:
            return 'That role does not exist.'
        response = await add_role(message, user, role)
    elif command == 'removerole':
        if len(args) < 2:
            return 'Please specify a user and role to remove.'
        # Prends l'user et le role
        user = discord.utils.get(message.guild.members, mention=args[0])
        if user is None:
            return 'That user does not exist.'
        role = discord.utils.get(message.guild.roles, name=args[1])

        response = await remove_role(message, user, role)
    elif command == 'createrole':
        if len(args) < 2:
            return 'Please specify a role name and permissions (in decimal format) to create a role.'
        role_name = args[0]
        permissions = discord.Permissions(permissions=int(args[1]))
        response = await create_role(message, role_name, permissions)
    elif command == 'deleterole':
        if len(args) == 0:
            return 'Please specify a role to delete.'
        role = discord.utils.get(message.guild.roles, name=args[0])
        if role is None:
            return 'That role does not exist.'
        response = await delete_role(message, role)
    elif command == 'listroles':
        response = await list_roles(message)
    elif command == 'listuserroles':
        if len(args) == 0:
            return 'Please specify a user to see their roles.'
        # Prend l'user
        user = discord.utils.get(message.guild.members, mention=args[0])
        if user is None:
            return 'That user does not exist.'
        response = await list_user_roles(message, user)
    else:
        response = 'Invalid command. Available commands: addrole, removerole, createrole, deleterole, listroles, listuserroles'
    await message.channel.send(response)

client.run('# A METTRE LA VOTRE #')

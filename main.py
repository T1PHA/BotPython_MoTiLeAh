import discord
from discord.ext import commands
import random

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

# Bot initialisation
bot = commands.Bot(command_prefix='!')

# Liste des Pokémon disponibles pour le combat
pokemon_list = ["Pikachu", "Bulbizarre", "Salamèche", "Carapuce", "Dracaufeu", "Mewtwo"]

# Fonction pour gérer un tour de combat
def combat_round(p1, p2):
    # Sélection aléatoire des attaques de chaque Pokémon
    p1_attack = random.randint(10, 20)
    p2_attack = random.randint(10, 20)

    # Détermination du Pokémon gagnant du tour
    if p1_attack > p2_attack:
        winner = p1
    elif p2_attack > p1_attack:
        winner = p2
    else:
        winner = None
    
    return (winner, p1_attack, p2_attack)

@bot.command()
async def battle(ctx, p1, p2):
    # Vérifier que les Pokémon entrés sont valides
    if p1 not in pokemon_list or p2 not in pokemon_list:
        await ctx.send("Un ou plusieurs des Pokémon entrés ne sont pas valides. Veuillez entrer des Pokémon valides à partir de la liste suivante : " + ', '.join(pokemon_list))
        return

    # Lancer un message pour annoncer le début du combat
    await ctx.send(f"Le combat entre {p1} et {p2} a commencé ! Que le meilleur gagne !")

    # Déterminer le nombre de tours de combat
    rounds = random.randint(3, 7)

    # Boucle pour gérer chaque tour de combat
    for i in range(rounds):
        (winner, p1_attack, p2_attack) = combat_round(p1, p2)
        if winner:
            await ctx.send(f"Tour {i + 1}: {winner} gagne avec une attaque de {p1_attack if winner == p1 else p2_attack}")
        else:
            await ctx.send(f"Tour {i + 1}: égalité avec des attaques de {p1_attack} pour {p1} et {p2_attack} pour {p2}")
    
    # Déterminer le gagnant final
    if p1_attack > p2_attack:
        await ctx.send(f"{p1} a gagné le combat avec une attaque finale de {p1_attack} contre {p2_attack} pour {p2} !")
    elif p2_attack > p1_attack:
        await ctx.send(f"{p2} a gagné le combat avec une attaque finale de {p2_attack} contre {p1_attack} pour {p1} !")
    else:
        await ctx.send(f"Le combat est terminé en égalité entre {p1} et {p2} avec des attaques finales de {p1_attack} pour {p1} et {p2_attack} pour {p2} !")

@client.event
async def on_message(message):
    if message.content.startswith('!mute'):
        user = message.mentions[0]
        role = discord.utils.get(message.guild.roles, name="Sanctionner")
        await user.add_roles(role)
        print("ajout role")
        await message.channel.send(f'{user.mention} a été mute.')
        print("L'utilisateur ne peut plus parler")
    if message.content.startswith('!unmute'):
        user = message.mentions[0]
        role = discord.utils.get(message.guild.roles, name="Sanctionner")
        await user.remove_roles(role)
        print("retrait role")
        await message.channel.send(f'{user.mention} a été unmute.')
        print("Utilisateur peut reparler")
    if message.content.startswith('!ban'):
        user = message.mentions[0]
        await user.ban()
        await message.channel.send(f'{user.mention} a été banni.')
        print("Utilisateur bannis")

client.run('# A METTRE LA VOTRE #')

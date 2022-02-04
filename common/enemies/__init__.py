# A list of all enemies
enemies = dict()
enemy_id = 0


def enemy_create(enemy):
    """Create an enemy"""
    global enemy_id
    enemies[enemy_id] = enemy
    enemy.id = enemy_id
    enemy_id = enemy_id + 1


def enemy_destroy(enemy):
    """Destroy an enemy"""
    global enemies
    enemies.pop(enemy.id)


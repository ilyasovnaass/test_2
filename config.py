from decouple import config

BOT_TOKEN = config('BOT_TOKEN')
DATABASE = config('DATABASE')    # указываем путь и имя файла, в котором физически будут храниться все данные. Если файла нет, SQL создаст его автоматически

TOKEN = config('TOKEN')
DATA_BASE = config('DATA_BASE')
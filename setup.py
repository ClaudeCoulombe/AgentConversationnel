from setuptools import setup

setup(name='AgentConversationnel',
      version='0.1',
      description='Agent conversationnel en français',
      url='https://github.com/ClaudeCoulombe/AgentConversationnel',
      authors=['Claude Coulombe'],
      authors_email=['claude.coulombe@gmail.com'],
      license='Apache 2',
      packages=['.'],
      package_data={
      'AgentConversationnel/DATA/': ['donnees.txt']},
      zip_safe=False)


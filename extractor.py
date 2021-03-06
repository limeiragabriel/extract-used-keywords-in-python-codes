import keyword, os

caminhos = [os.path.join('..', nome) for nome in os.listdir('..')]
arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
pyCodes = [arq for arq in arquivos if arq.lower().endswith(".py")]

# lista de operadores =====================================================
operators = ['+','-','*','/','//','**','%','>','>=','<','<=','==','!=']
#==========================================================================
# ==== lista de palavras reservadas encontradas ===========================
usedkw = []
#==========================================================================
#==== lista de operadores usados ==========================================
usedOperators = []
#==========================================================================

comentario = False
# loop pela lista de arquivos da pasta ====================================
for arq in pyCodes:
	# ===== lista de palavras reservadas ========
	reserved = keyword.kwlist
	#============================================
	file = open(arq, 'r')
	#=== loop pelo conteudo do arquivo ===

	for item in file.readlines():
		#==============================nao considera linhas comentadas============================
		if len(item) >= 3:
			if (item[0] == '#') or (item[1] == '#') or (item[2] == '#'):
				pass
			#=====================================================================================
			elif ((item.find('"""') >= 0) or (item.find("'''") >= 0)) and comentario == False:
				comentario = True
				pass

			elif ((item.find('"""') >= 0) or (item.find("'''") >= 0)) and comentario == True:
				comentario = False
				pass

			# se a linha nao for comentada:
			elif(comentario == False):
				# checa palavra por palavra se ela existe no arquivo ====
				for word in reserved:
					# se a palavra ja foi encontrada remove da lista para evitar nova busca desnecessaria
					if word in usedkw:
						reserved.remove(word)
					# busca a palavra e adiciona na lista de usadas caso haja
					else:
						# tratando casos na forma em que as palavras podem aparecer
						caseA = item.find(word+' ') #espaco vazio evita que pavras incorretas sejam adicionadas (exemplo importado != import)
						caseB = item.find(word+':') # casos como "else:"
						caseC = item.find(word+'(') # casos como if()
						caseD = item.find(')'+word+" ") # casos como if()or etc...
						caseE = item.find(':'+word+" ") # casos como if True:print
						# adiciona a lista caso haja posicoes ocupadas por palavras reservadas
						if caseA >= 0:
							if item[0] == word[0]:
								usedkw.append(word)
							elif item[caseA-1] == ' ':
								usedkw.append(word)
							elif item[caseA-1] == '\\':
								usedkw.append(word)
							elif item[caseA-2] == '\\' and ((caseA-1)=='t'):
								usedkw.append(word)
						elif caseB >= 0:
							usedkw.append(word)
						elif caseC >= 0:
							usedkw.append(word)
						elif caseD >= 0:
							usedkw.append(word)
						elif caseE >= 0:
							usedkw.append(word)
						#=========================================================================
				#verificacao para os operadores ===================================================
				for operator in operators:
					if operator in usedOperators:
						pass
					else:
						if item.find(operator) >= 0:
							usedOperators.append(operator)
			#==================================================================================

	#fecha o arquivo depois de verificar por completo ====================================
	file.close()
	#=====================================================================================

relatorio = open('relatorio.txt', 'w')

relatorio.write('\n'+'=================\nUsed Keywords:\n=================\n')
for item in usedkw:
	relatorio.write(item+'\n')
relatorio.write('\n=================\nUsed Operators:\n=================\n')
for item in usedOperators:
	relatorio.write(item+'\n')
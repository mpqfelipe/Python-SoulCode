import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from pymongo import MongoClient

def get_database():
    from pymongo import MongoClient

    CONNECTION_STRING = "mongodb+srv://user:jkgugA78@cluster1.bgw0k.mongodb.net/myFirstDatabase"

    from pymongo import MongoClient

    client = MongoClient(CONNECTION_STRING)  #conexão com o cliente

    return client["socioeconomico"]  #base de dados
    
dbname = get_database()
collection_name = dbname["venezuela2021"]

detalhes_itens = collection_name.find()
# consulta o db no Mongo, coloca todos os dados do database nessa variavel.

df = pd.DataFrame(list(detalhes_itens)) #criei um df com o banco de dados

perfil = df[["gender", "age", "geography", "financial_situation"]]  # criando um df apenas com as chaves interessantes para o perfil


###############################################################################################################


###Criar gráfico que mostra a quantidade de pessoas entrevistadas em cada faixa etária
def faixaetaria(perfil):
  age_qtd = (perfil["age"]).value_counts()  # crio uma variavel em que quantifica cada faixa etaria obtida na pesquisa
  print(age_qtd)  # exemplo: 1304 pessoas tem idade de 26 a 35 anos
  plt.style.use("ggplot")
      
  age_qtd.plot.barh()  # defino o tipo de grafico
  plt.title("Número de pessoas entrevistadas por faixa etária")  # adiciona titulo
  plt.xlabel("Número de pessoas")  # nomeia eixo x
  plt.ylabel("Faixa etária")  # nomeia eixo y
  plt.show()  # exibe o grafico
    

###Criar grafico com gênero e idade no formato barras
def generoidade(df):
  perfil2 = df[["gender", "age"]]
  print(perfil2)
      
  plt.style.use("ggplot")
  graf = (perfil2).value_counts()
  print(graf)
  graf.plot.barh()
  plt.title("Número de pessoas entrevistadas por gênero e faixa etária")  # adiciona titulo
  plt.xlabel("Número de pessoas")  # nomeia eixo x
  plt.ylabel("Gênero e Faixa etária")  # nomeia eixo y
  plt.show()  # exibe o grafico
    
  
###Criar grafico de Gênero no formato Pizza:
def genero(perfil):
  gen_qtd = (perfil["gender"]).value_counts()  # crio uma variavel em que quantifica cada genero obtido na pesquisa
  print(gen_qtd)
  df1 = gen_qtd.iloc[[2,3,4]]

  df2=gen_qtd.drop(gen_qtd.index[[2,3,4]]) #aqui estou eliminando essas linhas para colocar o resultado da soma em uma linha só
  print(df2) #só tem genero female e male
  df2.loc['Others: Non-Binary, Non Available, Prefer not to Answer'] = sum(df1)  # acrescento uma nova linha com index others e o valor da soma.

  plt.style.use("ggplot")
  df2.plot.pie() # defino o tipo de grafico
  plt.title("Número de pessoas entrevistadas por gênero")  # adiciona titulo
  plt.show()  # exibe o grafico
    
    
###Criar gráfico das situações financeiras da pessoas entrevistadas pela pesquisa
def sitfin(perfil):
  sitfin = (perfil["financial_situation"]).value_counts()  # crio uma variavel em que quantifica a sit financeira de cada pessoa da pesquisa
  print(sitfin)  # exemplo: 1445 só conseguem custear comida e nada mais

  plt.style.use("ggplot")
  sitfin.plot.pie(autopct = "%1.1f%%",  ylabel='')
  plt.title("Situação financeira das pessoas entrevistadas")  # adiciona titulo
  plt.show()  # exibe o grafico


###Criar gráfico que mostra a quantidade de pessoas entrevistadas por cada região em que vivem
def geografia(perfil):
  geography = (perfil["geography"]).value_counts()  # crio uma variavel em que quantifica cada faixa etaria obtida na pesquisa
  print(geography)  # exemplo: 1304 pessoas tem idade de 26 a 35 anos

  plt.style.use("ggplot")
  geography.plot.barh(color = "lightsalmon")  # defino o tipo de grafico
  plt.title("Número de pessoas entrevistadas por região em que vivem")  # adiciona titulo
  plt.xlabel("Número de pessoas")  # nomeia eixo x
  plt.ylabel("Região")  # nomeia eixo y
  plt.show()  # exibe o grafico
    
 
###Criar um grafico em que mostra a relação entre a região e as pessoas que são muito vulneraveis financeiramente
def relregiaositfin(df):
  perfil3 = df[["geography", "financial_situation"]] #cria dataframe com as chaves de interesse
  aux = perfil3[(perfil3['financial_situation'] == 'I cannot afford enough food for my family')] #crio uma variavel em que recebe a sit fin desejada
  print(aux.groupby('geography').count()) #relaciona a sit financeira desejada com a geografia e faz a contagem do num de pessoas.
  graf1 = aux.groupby('geography').count() #crio uma variavel que relaciona a auxiliar (sit fin) com a geografia e quantifica
            
  graf1.plot()
  plt.title("Região em que vivem as pessoas que não conseguem comprar comida suficiente para a família") #Não consigo comprar comida suficiente para a minha família.
  plt.ylabel("Número de pessoas")
  plt.xlabel("Geografia")
  plt.show()
    
  
def favoVulne(df):
    #perfil de pessoa na situação mais confortavel, universidade/faculdade/pos graduação completa ou nao  e criança com acesso a internet.
    df_fvvn = df[['_id', 'financial_situation', 'education', 'do_children_have_internet_connection']]
    docTotais = 4436
    
    favo1 = len(df_fvvn[(df_fvvn['financial_situation'] == "I can comfortably afford food, clothes, and furniture, and I have savings") & (df_fvvn['education'] == "University or college degree completed") & (df_fvvn['do_children_have_internet_connection'] == '1')])
    favoPorcent1 = (favo1 * 100) / docTotais
    
    favo2 = len(df_fvvn[(df_fvvn['financial_situation'] == "I can comfortably afford food, clothes, and furniture, and I have savings") & (df_fvvn['education'] == "Some university or college") & (df_fvvn['do_children_have_internet_connection'] == '1')])
    favoPorcent2 = (favo2 * 100) / docTotais
    
    favo3 = len(df_fvvn[(df_fvvn['financial_situation'] == "I can comfortably afford food, clothes, and furniture, and I have savings") & (df_fvvn['education'] == "Post-graduate education") & (df_fvvn['do_children_have_internet_connection'] == '1')])
    favoPorcent3 = (favo3 * 100) / docTotais
    
    favo4 = len(df_fvvn[(df_fvvn['financial_situation'] == "I can comfortably afford food, clothes, and furniture, and I have savings") & (df_fvvn['education'] == "Post graduate") & (df_fvvn['do_children_have_internet_connection'] == '1')])
    favoPorcent4 = (favo4 * 100) / docTotais
    
    pessoasFavoravel = favo1 + favo2 + favo3 + favo4
    pessoasFavoravelPorc = favoPorcent1 + favoPorcent2 + favoPorcent3 + favoPorcent4
    print(f"{pessoasFavoravel} documentos apontaram que tem condições financeiras confortaveis, alto nivel educacional e criança com acesso a internet \nIsso representa {pessoasFavoravelPorc} % da amostra total\n")
    
    #perfil de pessoa na situação mais vulneravel, baixo nivel educacional  e criança sem acesso a internet
    vulne1 = len(df_fvvn[(df_fvvn['financial_situation'] == "I cannot afford enough food for my family") & (df_fvvn['education'] == "No formal education") & (df_fvvn['do_children_have_internet_connection'] == '0')])
    vulnePorcent1 = (vulne1 * 100) / docTotais
    
    vulne2 = len(df_fvvn[(df_fvvn['financial_situation'] == "I cannot afford enough food for my family") & (df_fvvn['education'] == "Some primary education") & (df_fvvn['do_children_have_internet_connection'] == '0')])
    vulnePorcent2 = (vulne2 * 100) / docTotais

    vulne3 = len(df_fvvn[(df_fvvn['financial_situation'] == "I cannot afford enough food for my family") & (df_fvvn['education'] == "Primary school completed") & (df_fvvn['do_children_have_internet_connection'] == '0')])
    vulnePorcent3 = (vulne3 * 100) / docTotais


    pessoasVulneraveis = vulne1 + vulne2 + vulne3 
    pessoasVulneraveisPorc = vulnePorcent1 + vulnePorcent2 + vulnePorcent3
    print(f"{pessoasVulneraveis} documentos apontaram que não tem condições de custear alimentação suficiente, tem baixo nivel educacional e criança sem acesso a internet \nIsso representa {pessoasVulneraveisPorc} % da amostra total\n")
    
    grupos = ['Condição Mais \n Favorável', 'Condição Menos \n Favorável']
    valores = [pessoasFavoravel, pessoasVulneraveis]
    plt.title('OS DOIS PERFIS EXTREMOS')
    plt.ylabel('Numero de formularios')
    plt.bar(grupos, valores)
    plt.show()
    

def desfavoravel(df):
    
    df_vul = df[['_id', 'financial_situation', 'education', 'do_children_have_internet_connection']]
    docTotais = 4436

    semAlimentacao = len(df_vul[(df_vul['financial_situation'] == "I cannot afford enough food for my family")])

    #perfil de pessoa na situação mais vulneravel, universidade/faculdade/pos graduação completa ou nao  e criança sem acesso a internet
    alto1 = len(df_vul[(df_vul['financial_situation'] == "I cannot afford enough food for my family") & (df_vul['education'] == "University or college degree completed") & (df_vul['do_children_have_internet_connection'] == '0')])
    altoPorcent1 = (alto1 * 100) / docTotais
    
    alto2 = len(df_vul[(df_vul['financial_situation'] == "I cannot afford enough food for my family") & (df_vul['education'] == "Some university or college") & (df_vul['do_children_have_internet_connection'] == '0')])
    altoPorcent2 = (alto2 * 100) / docTotais

    alto3 = len(df_vul[(df_vul['financial_situation'] == "I cannot afford enough food for my family") & (df_vul['education'] == "Post-graduate education") & (df_vul['do_children_have_internet_connection'] == '0')])
    altoPorcent3 = (alto3 * 100) / docTotais

    alto4 = len(df_vul[(df_vul['financial_situation'] == "I cannot afford enough food for my family") & (df_vul['education'] == "Post graduate") & (df_vul['do_children_have_internet_connection'] == '0')])
    altoPorcent4 = (alto4 * 100) / docTotais

    pessoasEducAlta = alto1 + alto2 + alto3 + alto4
    educAlta = altoPorcent1 + altoPorcent2 + altoPorcent3 + altoPorcent4

    print(f"{pessoasEducAlta} documentos apontaram não ter condições de custear alimentação suficiente, tem alto nivel educacional e criança sem acesso a internet \nIsso representa {educAlta} % da amostra total\n")

    #perfil de pessoa na situação mais vulneravel, educação secundaria  e criança sem acesso a internet
    med1 = len(df_vul[(df_vul['financial_situation'] == "I cannot afford enough food for my family") & (df_vul['education'] == "Secondary school/ high school completed") & (df_vul['do_children_have_internet_connection'] == '0')])
    medPorcent1 = (med1 * 100) / docTotais
    
    med2 = len(df_vul[(df_vul['financial_situation'] == "I cannot afford enough food for my family") & (df_vul['education'] == "Some secondary school / high school") & (df_vul['do_children_have_internet_connection'] == '0')])
    medPorcent2 = (med2 * 100) / docTotais

    med3 = len(df_vul[(df_vul['financial_situation'] == "I cannot afford enough food for my family") & (df_vul['education'] == "Secondary/high school") & (df_vul['do_children_have_internet_connection'] == '0')])
    medPorcent3 = (med3 * 100) / docTotais

    pessoasEducMedia = med1 + med2 + med3
    educMedia = medPorcent1 + medPorcent2 + medPorcent3
    print(f"{pessoasEducMedia} documentos apontaram não ter condições de custear alimentação suficiente, tem medio nivel educacional e criança sem acesso a internet \nIsso representa {educMedia} % da amostra total\n")


    #perfil de pessoa na situação mais vulneravel, educação tecnica completa ou nao (agrupadas) e criança sem acesso a internet
    tec1 = len(df_vul[(df_vul['financial_situation'] == "I cannot afford enough food for my family") & (df_vul['education'] == "Technical school diploma or degree completed") & (df_vul['do_children_have_internet_connection'] == '0')])
    tecPorcent1 = (tec1 * 100) / docTotais
    
    tec2 = len(df_vul[(df_vul['financial_situation'] == "I cannot afford enough food for my family") & (df_vul['education'] == "Some technical education (e.g polytechnic school") & (df_vul['do_children_have_internet_connection'] == '0')])
    tecPorcent2 = (tec2 * 100) / docTotais

    tec3 = len(df_vul[(df_vul['financial_situation'] == "I cannot afford enough food for my family") & (df_vul['education'] == "Technical school") & (df_vul['do_children_have_internet_connection'] == '0')])
    tecPorcent3 = (tec3 * 100) / docTotais

    pessoasEducTecnica = tec1 + tec2 + tec3
    educTecnica = tecPorcent1 + tecPorcent2 + tecPorcent3
    print(f"{pessoasEducTecnica} documentos apontaram  não ter condições de custear alimentação suficiente para a familia, tem nivel educacional técnico e criança sem acesso a internet \nIsso representa {educTecnica} % da amostra total\n")
    
    grupos = ['Não conseguem \nCustear alimentação', 'Ensino Superior', 'Ensino Médio', 'Ensino Tecnico']
    valores = [semAlimentacao, pessoasEducAlta, pessoasEducMedia, pessoasEducTecnica]
    plt.title('RELAÇÃO VULNERABILIDADE X NIVEL EDUCACIONAL')
    plt.ylabel('Numero de formularios')
    plt.bar(grupos, valores)
    plt.show()


def intAcess1(df):
    #se a criança tem acesso a internet e tem energia eletrica consistentes, se perde aula. se nao tem acesso, esta com aula presencial
    df_vul = df[['_id', 'do_children_have_internet_connection', 'does_home_shows_severe_deficit_of_electricity', 'does_home_shows_severe_deficit_of_internet', 'do_children_3_to_17_yrs_miss_virtual_class_due_to_lack_of_electricity', 'are_children_attending_face_to_face_classes', 'are_children_being_teached_by_unqualified_people']]
    docTotais = 4436
    
    perfil1 = len(df_vul[(df_vul['does_home_shows_severe_deficit_of_electricity'] == '0') & (df_vul['does_home_shows_severe_deficit_of_internet'] == '0') & (df_vul['do_children_have_internet_connection'] == '1') & (df_vul['do_children_3_to_17_yrs_miss_virtual_class_due_to_lack_of_electricity'] == '0')])
    porcentagem1 = (perfil1 * 100) / docTotais
    print(f"{perfil1} documentos apontaram que há crianças sem problemas de conexão com internet ou falta de energia eletrica e não perdem aulas por estes motivos.\nIsso representa {porcentagem1} % da amostra total\n")
    
    perfil2 = len(df_vul[(df_vul['does_home_shows_severe_deficit_of_electricity'] == '1') | (df_vul['does_home_shows_severe_deficit_of_internet'] == '1') & (df_vul['do_children_have_internet_connection'] == '1') & (df_vul['do_children_3_to_17_yrs_miss_virtual_class_due_to_lack_of_electricity'] == '1')])
    porcentagem2 = (perfil2 * 100) / docTotais
    print(f"{perfil2} documentos apontaram que há crianças com problemas de conexão com internet ou falta de energia eletrica e perdem aulas por estes motivos.\nIsso representa {porcentagem2} % da amostra total\n")
    
    perfil3 = len(df_vul[(df_vul['are_children_attending_face_to_face_classes'] == '1') | (df_vul['does_home_shows_severe_deficit_of_internet'] == '1') & (df_vul['do_children_have_internet_connection'] == '0')])
    porcentagem3 = (perfil3 * 100) / docTotais
    print(f"{perfil3} documentos apontaram que há crianças sem acesso a internet ou tem problemas de conexão e estão tendo aulas presenciais.\nIsso representa {porcentagem3} % da amostra total\n")
    
    perfil4 = len(df_vul[(df_vul['are_children_attending_face_to_face_classes'] == '0') & (df_vul['does_home_shows_severe_deficit_of_internet'] == '1') & (df_vul['do_children_have_internet_connection'] == '0')])
    porcentagem4 = (perfil4 * 100) / docTotais
    print(f"{perfil4} documentos apontaram que há crianças sem acesso a internet ou tem problemas de conexão e não estão tendo aulas presenciais.\nIsso representa {porcentagem4} % da amostra total\n")

    perfil5 = len(df_vul[(df_vul['are_children_attending_face_to_face_classes'] == '0') & (df_vul['does_home_shows_severe_deficit_of_internet'] == '1') & (df_vul['do_children_have_internet_connection'] == '0') & (df_vul['are_children_being_teached_by_unqualified_people'] == '1')])
    porcentagem5 = (perfil5 * 100) / docTotais
    print(f"{perfil5} documentos apontaram que há crianças sem acesso a internet ou tem problemas de conexão e não estão tendo aulas presenciais \n e estão sendo ensinadas por pessoas sem qualificação.Isso representa {porcentagem5} % da amostra total\n")
    
    
    grupos = ['Não perdem \naula virtual', 'Problemas técnicos \nPerdem aula virtual', 'Sem acesso \nAula presencial', 'Sem aula virtual\n nem presencial', 'Aula com pessoas\n não qualificadas']
    valores = [perfil1, perfil2, perfil3, perfil4, perfil5]
    plt.title('RELAÇÃO ACESSOS A INTERNET E ENERGIA x AULA VIRTUAL/PRESENCIAL')
    plt.ylabel(' Numero de formularios')
    plt.bar(grupos, valores)
    plt.show()


def inseg(df):#Grafico barra alimentação

    data=df[["financial_situation","do_children_3_and_17_yrs_receive_regular_school_meals"]]

    aux = data[(data['do_children_3_and_17_yrs_receive_regular_school_meals'] == "No")]
    graf = aux.groupby('financial_situation').count()

    graf.plot.barh()
    plt.title("Insegurança alimentar x Situação Financeira") 
    plt.ylabel("")
    L=plt.legend(bbox_to_anchor=(1.1,1.1),\
        bbox_transform=plt.gcf().transFigure)
    L.get_texts()[0].set_text('Crianças que recebem comida na escola')
    plt.savefig('temp.png')
    plt.show()    


def evesao(df): #Grafico barra para evasão escolar

  data=df[["education","were_children_3_to_17_yrs_enrolled_and_did_not_return_to_school"]]

  aux = data[(data['were_children_3_to_17_yrs_enrolled_and_did_not_return_to_school'] == "0")]
  graf = aux.groupby('education').count()


  graf.plot.barh()
  plt.title("Evasão escolar x nível educacional do responsável") 
  plt.ylabel("")
  L=plt.legend(bbox_to_anchor=(1.1,1.1),\
    bbox_transform=plt.gcf().transFigure)
  L.get_texts()[0].set_text('Crianças que não retornaram a escola')
  plt.savefig('temp.png')
  plt.show()

#retorna um gráfico do grau de escolaridade das pessoas que responderam o questionário
def educacao(df):
    df_new = df[['education']]
    
    #destaca a coluna com o maior valor
    explode = (0.1, 0, 0, 0, 0, 0, 0, 0)
    colors = ['#FFFF00', '#800080','#B22222','#483D8B','#FA8072','#CD853F','#2E8B57', '#FF4500']
    
    labels = ['Graduação em faculdade completa','Segundo grau (Ensino médio) completo', 'Diploma de escola técnica ou algum título completo','Possui alguma educação universitária','Possui alguma educação técnica','Possui alguma educação secundária/ensino médio', 'Pós-graduação completa','Outros']

    #gráfico de pizza da educação
    graf = (df_new["education"]).value_counts()
    
    # autopct = rotular as fatias com seu valor numérico
    # shadow = sombra | 
    graf2 = graf
    soma = sum(graf2.iloc[[12, 13, 14, 15, 8, 11, 10, 7, 9]]) 
    graf2 = graf2.drop(graf2.index[[12, 13, 14, 15, 8, 11, 10, 7, 9]])   
    graf2.loc['Others'] = soma

    graf2.plot.pie(autopct='%1.1f%%', explode= explode, shadow=True, startangle = 90, labels=labels, ylabel='', colors = colors) 
    
    plt.title('Educação na Venezuela')
    plt.show()

#retorna um gráfico da situação financeira em relação a educação de pessoas que possuem algum diploma 
def financial_situation_education(df):

    colunas = ['financial_situation', 'education']
    df_new = df.filter(items = colunas)
    
    aux = df_new[(df_new['education'] == 'University or college degree completed') | (df_new['education'] == 'Secondary school/ high school completed') | (df_new['education'] ==  'Technical school diploma or degree completed')]
    
    graf = aux.groupby('financial_situation').count()

    graf.plot.pie(autopct='%1.1f%%', shadow=True, startangle = 90, subplots=True, ylabel='')

    #L=plt.legend(bbox_to_anchor=(1.1,1.0),\
    #bbox_transform=plt.gcf().transFigure)

    L = plt.legend(bbox_to_anchor=(1.9, 1.1))

    #L.get_texts()[0].set_text('Consigo custear alimentos e despesas regulares, mas nada além disso.','Consigo custear alimento, mas nada além disso.','Consigo custear alimentos, despesas regulares e roupas, mas nada além disso', 'Consigo confortavelmente comprar alimentos, roupas e móveis e tenho economias. ', 'Consigo confortavelmente comprar alimentos, roupas e móveis, mas não tenho economias.','Não consigo comprar comida suficiente para a minha família.', 'Prefiro não responder')

    plt.savefig('temp.png') 
    plt.title('Situação finaceira X Educação')
    plt.show()


#Chamando as funções 


#faixaetaria(perfil)  #gráfico que mostra a quantidade de pessoas entrevistadas em cada faixa etária
#generoidade(df)  #grafico que exibe gênero e idade das pessoas entrevistadas no formato barras
#genero(perfil)  #grafico que mostra a qtd de pessoas por gênero no formato Pizza
#sitfin(perfil)  #gráfico das situações financeiras das pessoas entrevistadas na pesquisa
#geografia(perfil) #gráfico que mostra a quantidade de pessoas entrevistadas por cada região em que vivem
#relregiaositfin(df) #grafico mostra a relação entre a região e as pessoas que são vulneraveis financeiramente


#favoVulne(df) # apresenta perfis opostos: mais condições desfavoraveis e mais condições favoraveis
#intAcess1(df) #Relaciona acesso a internet e modalidade de aulas
#desfavoravel(df) # apresenta relação de pessoas que nao conseguem custear alimentação e nivel educacional alto e medio


#inseg(df) #grafico que compara a sitação financeira com alimentação na escola
#evesao(df) #grafico que compara evesão escolar com o nivel educacional do responsável


#educacao(df) #mostra o gráfico da educação 
#financial_situation_education(df) #mostra o gráfico da situação financeira e educação

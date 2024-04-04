import streamlit as st
import pandas as pd
from io import StringIO
import re



st.set_page_config(
    page_title="TRAIÇÃO X - Analisador de Espectro Relacional",
    page_icon="💘",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        
        'Get Help': 'https://mailto:rodneyneville@gmail.com',
        'Report a bug': 'https://mailto:rodneyneville@gmail.com',
        'About': "# Desenvolvido por Rodney *Neville* aproveite!"
    }
)
# Função para verificar padrões de flerte
def verificar_padroes(texto, padroes):
    import re
    for padrao in padroes:
        if re.search(padrao, texto, re.IGNORECASE):
            return True
    return False

# Padrões de flerte
padroes_flerte = [
    r"\blindo(a)?\b",
    r"\badoro seu sorriso\b",
    r"\bsinto (sua )?falta\b",
    r"\bsaudades?\b",
    r"\bcasad(o|a)\b",
    r"\bbeijos?\b",
    r"\bte quero\b",
    r"\bte amo\b",
    r"\bgosto de (você|vc)\b",
    r"\bencontr(ar|o|amos|inho)?\b",
    r"\bnoss(o|a|os|as)\b",
    r"\breservado(a)?\b",
    r"\bquero (você|vc)\b",
    r"\bamor\b",
    r"\bsexo\b",
    r"\bprazer\b",
    r"\bme chamou\b",
    r"\bgost(o|ei|amos|aria|oso|osa|ando)\b",
    r"\bvamos (sair|nos)\b",
    r"\bsequestrar\b",
    r"\bquer\?\b",
    r"\baqui em casa\?\b",
    r"\bsozinh(o|a)\b",
    r"\bte possuir\b",
    r"\bnudes?\b",
    r"\bmanda(r)? foto(s)?\b",
    r"\bmaravilhos(o|a)\b",
    r"\bdescobriu?\b",
    r"\badmirado(r|ra)\b",
    r"\bestá pensando\b",
    r"\bestá sentindo\b",
    r"\bciume(ento|menta)\b",
    r"😍",
    r"😘",
    r"🥰",
    r"💕",
    r"💋",
    r"❤️",
    r"💘",
]

def gerar_tabela_html(df, periodo):
    html = '<h4>Mensagens com Marcação</h4><table style="font-size: 12px;">'
    html+= '<p>'+periodo+'</p>'
    colunas_exibidas = ['Dia e Horário', 'Autor', 'Texto']
    # Adicionando o cabeçalho da tabela
    html += '<tr>' + ''.join(f'<th style="white-space: nowrap;">{col}</th>' for col in colunas_exibidas) + '</tr>'

    for _, row in df.iterrows():
        cor_fundo = 'background-color: yellow; color:black' if row['x'] else ''
        html += '<tr style="' + cor_fundo + '">' + ''.join(f'<td>{row[col]}</td>' for col in colunas_exibidas) + '</tr>'
    html += '</table>'
    return html


# Função para verificar padrões de flerte
def verificar_padroes(texto, padroes):
    for padrao in padroes:
        if re.search(padrao, texto, re.IGNORECASE):
            return 1
    return 0

# Função para aplicar o estilo
def destaca_linhas_presentes(linha):
    #if linha['x']:
        return ['background-color: yellow']*len(linha)
    #else:
     #   return ['']*len(linha)

# Função principal da aplicação Streamlit
def main():
    st.title("TRAIÇÃO X - Analisador de Espectro Relacional")

    # Carregamento do arquivo de conversas
    uploaded_file = st.file_uploader("Carregue o arquivo de conversas (WhatsApp)", type="txt")
    
    # Inputs de texto para filtro
    nome1 = st.text_input("Nome da Pessoa 1:")
    nome2 = st.text_input("Nome da Pessoa 2:")

    if (uploaded_file is not None and nome1 is not None and nome2 is not None):
        # Leitura do arquivo
        conversas = StringIO(uploaded_file.getvalue().decode("utf-8"))
        #df = pd.read_csv(conversas, sep=" - ", names=["Data", "Autor e Texto"], engine="python")
        df = pd.read_csv(conversas, index_col=False, encoding='utf8', on_bad_lines='skip',sep=" - ", names=["Data", "Autor e Texto"], engine="python").reset_index(drop=True)

        # Separando o autor do texto
        padrao = r'^({}|{}): (.*)$'.format(nome1, nome2)
        df[["Autor", "Texto"]] = df["Autor e Texto"].str.extract(padrao)

        # Filtrando linhas se a Coluna Data conter uma data  
        padrao_data_hora = r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$'
        df = df[df['Data'].str.match(padrao_data_hora)]

        # Removendo linhas com qualquer valor nulo
        df.dropna(inplace=True)


        # Removendo Autor e Texto
        df.drop(columns=["Autor e Texto"], inplace=True)

        #Filtrando para apenas formato correto de data seja utilizada
        df = df[df['Data'].str.match(padrao_data_hora)]

        # Convertendo a coluna 'Data' para o tipo datetime
        df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y %H:%M')
        df['Dia e Horário'] = df['Data'].dt.strftime('%d %H:%M:%S')

        #Criando coluna ano/mes
        df['Ano_Mes'] = df['Data'].dt.to_period('M')

        #Filtrando período data > Outubro/23
        #df = df[df['Data'] > pd.Timestamp('2023-10-01 00:00:00')].reset_index(drop=True)


         
        # Extração de ano e mês
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
        df['Ano'] = df['Data'].dt.year
        df['Mes'] = df['Data'].dt.month
        
        # Itens de menu para seleção de ano e mês
        anos = df['Ano'].dropna().unique()
        anos.sort()
        ano_selecionado = st.selectbox('Selecione o ano:', anos)

        meses = df[df['Ano'] == ano_selecionado]['Mes'].unique()
        meses.sort()
        mes_selecionado = st.selectbox('Selecione o mês:', meses)

        # Filtragem do DataFrame
        df_filtrado = df[(df['Ano'] == ano_selecionado) & (df['Mes'] == mes_selecionado)]
        df_traicao = df_filtrado

        
        # Botão para aplicar a detecção de padrões
        if st.button('Detectar Interesse Amoroso'):
            df_traicao['Interesse_Amoroso'] = df_traicao['Texto'].apply(lambda x: verificar_padroes(str(x), padroes_flerte))
            df_traicao = df_traicao[df_traicao['Interesse_Amoroso'] == 1]
            st.write("Mensagens Com Nível Comprometedor")
            st.write(df_traicao)

            # Criando uma coluna 'Presente_na_Outra_Tabela' em df_filtrado
            df_filtrado['x'] = df_filtrado.index.isin(df_traicao.index)
            df_filtrado.style.apply(destaca_linhas_presentes, axis=1)

            # Gerando a tabela HTML e exibindo no Streamlit
            tabela_html = gerar_tabela_html(df_filtrado, str(mes_selecionado) + "/" + str(ano_selecionado))
            st.markdown(tabela_html, unsafe_allow_html=True)
        else:

            # Exibição da tabela filtrada
            st.write("Mensagens de " + str(mes_selecionado) + "/" + str(ano_selecionado))
            colunas_exibidas = ['Data', 'Autor', 'Texto']
            df_exibido = df_filtrado[colunas_exibidas]
            
            df_estilizado = df_exibido.style.applymap(lambda x: 'white-space: nowrap;')
            # Exibindo o DataFrame estilizado no painel
            st.dataframe(df_estilizado)

            #st.write(df_exibido)



if __name__ == "__main__":
    main()

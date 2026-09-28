# Base de conhecimento: guia de leitura para o Relatório Parcial

Guia **focado** para escrever as seções do `Relatório Parcial.docx` em 3 dias. Ele não redige o relatório.
Para cada seção há: **o que ler** (com página ou seção exata), **o que tirar dali** e **a referência ABNT** já
formatada (lista completa no fim, seção 7).

Legenda: ★ = leitura obrigatória; ☆ = opcional, só se sobrar tempo; 📄 = arquivo já nesta pasta.

> **Como tudo foi conferido (28 set. 2026).** A rede deste ambiente bloqueou a abertura direta dos sites.
> Os dados bibliográficos foram conferidos nos registros das editoras e dos indexadores (IEEE Xplore,
> ScienceDirect, ACM DL, Springer, PMC, JMLR, NeurIPS, SBC-SOL), e as estatísticas no texto das páginas
> citadas, em pelo menos duas fontes quando possível. O que não pôde ser confirmado está marcado **[confira]**.
> **Abra cada URL uma vez antes de citar**, principalmente as estatísticas (seção 1).

---

## 0. Antes de começar: 4 problemas no `Relatório Parcial.docx`

1. **O Resumo contradiz o próprio projeto.** Ele diz que os modelos "são otimizados em métricas de acurácia,
   precisão, sensibilidade...". A análise exploratória (`analise_exploratoria.ipynb`, seções 2 e 8) mostra que
   um classificador que nunca aponta fraude tem **99,833% de acurácia** e recall zero. A métrica principal do
   projeto é a **Average Precision (AP)**, com ROC-AUC como secundária e o limiar escolhido por F2. A acurácia
   não pode aparecer como métrica de otimização. Ela pode aparecer só como exemplo do porquê não usá-la.
   Toda a literatura da seção 3.3 abaixo sustenta isso.
2. **As referências do modelo são de outro trabalho.** Piletti, Boyer, D'Ambrósio, Kubo, Hart-Davis e
   Ribeiro são exemplos do template (educação matemática). Apague-as.
3. **Normas desatualizadas no template.** A NBR 6023 vigente é a de **2018** (não 2002), e a NBR 14724 vigente é
   a de **2011** (não 2002). Uma diferença prática da 6023:2018: a URL vem sem `< >`
   ("Disponível em: https://..."). Se o tutor exigir a formatação do template, siga o tutor.
4. **O dataset não é brasileiro.** São transações de portadores **europeus**, de setembro de 2013 (DAL POZZOLO
   et al., 2015, p. 6). Na introdução, os números do Brasil justificam a **relevância do problema**, não a
   origem dos dados. Deixe isso explícito na delimitação.

---

## 1. Introdução e Justificativa: números citáveis (dia 1, ~1 h)

Não precisa ler os relatórios inteiros; os números abaixo já foram localizados. Escolha 3 ou 4.

| Fato | Número | Fonte |
|---|---|---|
| Pagamentos com cartão no Brasil em 2025 | **R$ 4,5 trilhões** (+10,1% sobre 2024); **48,1 bilhões** de transações (+5,4%) | ABECS (2026) |
| Pagamentos com cartão em 2024 (comparação) | R$ 4,1 tri (+10,9%); 45,7 bi de transações | ABECS (2026) |
| Perdas com golpes e fraudes bancárias no Brasil | **R$ 10,1 bilhões em 2024** (+17% sobre R$ 8,6 bi em 2023) | FEBRABAN, divulgado por PODER360 (2025) |
| Tentativas de fraude contra bancos e cartões (Brasil, 2024) | **53,4%** de todas as tentativas; prejuízo potencial de até **R$ 51,6 bi** | SERASA EXPERIAN (2025) |
| Tipo de fraude mais comum entre as vítimas (Brasil, 2024) | "Uso indevido de cartão de crédito": **47,9%**; 50,7% dos brasileiros foram vítimas | SERASA EXPERIAN (2025) |
| Estelionatos registrados no Brasil em 2025 | **2.261.055** (+2,7% sobre 2024; +429,8% desde 2018; 258 golpes por hora) | FBSP (2026) |
| Transações bancárias (Brasil, 2025) | **240,8 bi**, 78% pelo celular; orçamento de tecnologia de R$ 50,4 bi em 2026 | FEBRABAN (2026) |
| Perdas mundiais com fraude em cartão | **US$ 33,41 bi em 2024**; projeção de US$ 41,06 bi em 2030 | NILSON REPORT (2026) |
| Fraude em pagamentos na Europa (EEE) | **€ 4,2 bi em 2024** (€ 3,5 bi em 2023); cartões, cerca de € 1,3 bi | EBA; ECB (2025) |

**Contexto legal (para a justificativa e a delimitação):**
- **LGPD** (Lei nº 13.709/2018): art. 5º, III e XI (dado anonimizado e anonimização) e **art. 12** (dado
  anonimizado não é dado pessoal, salvo se a anonimização puder ser revertida com esforço razoável). Serve para
  explicar por que o dataset vem com atributos PCA (V1 a V28). Cuidado: PCA sozinho não garante anonimização;
  o argumento é que a base é pública e sem identificadores.
- **Resolução Conjunta CMN/BCB nº 6, de 23 maio 2023**: obriga as instituições autorizadas a compartilhar dados
  sobre indícios de fraude (vigência a partir de 1º nov. 2023). Mostra que o combate à fraude é prioridade
  regulatória no Brasil.

**Leitura curta para dar o "tom" da introdução:**
- ★ 📄 `DalPozzolo_2014_Learned_Lessons_Credit_Card_Fraud.pdf`: **seção 1 (p. 2) e seção 3 até 3.2 (p. 3-5)**, cerca de 15 min.
  Por que detectar fraude é difícil: desbalanceamento extremo, mudança de padrão ao longo do tempo (*concept drift*)
  e custo da investigação manual.
- ★ CHERIF et al. (2023), revisão sistemática, acesso aberto: leia **só o resumo e a introdução**. Serve para citar
  que o tema é atual e muito pesquisado.
  https://www.sciencedirect.com/science/article/pii/S1319157822004062

---

## 2. Objetivos, Justificativa e Delimitação (dia 1, ~30 min)

Não há leitura nova aqui; use os fatos da seção 1 e estes pontos de delimitação, todos documentados no projeto:

- **Dados**: 284.807 transações em 2 dias (set. 2013), 492 fraudes (0,172%) (DAL POZZOLO et al., 2015, p. 6).
  Após remover 1.081 duplicatas: 283.726 transações e 473 fraudes (0,167%) (`analise_exploratoria.ipynb`, seção 1).
- **Atributos**: V1 a V28 (componentes PCA anonimizadas), `Amount` e `Horas_Dia` (derivada de `Time`).
- **Modelos**: SGDClassifier (linear), LightGBM (boosting de árvores) e MLP (rede neural rasa).
- **Fora do escopo**: implantação em produção, dados brasileiros, custo real de cada erro (os custos não são
  conhecidos), interpretabilidade dos atributos V (anonimizados).
- **Verbos para os objetivos**: o template (seção 2.1) já lista os verbos por tipo.

---

## 3. Fundamentação teórica (dia 2, ~4 h no total)

### 3.1 O problema: fraude em cartão com aprendizado de máquina (~45 min)
- ★ 📄 `DalPozzolo_2015_Calibrating_Probability_Undersampling.pdf`: **leia só a seção VI (p. 6, parágrafo do
  "Credit-card")**. É o artigo que o Kaggle pede para citar como fonte do dataset. Desta seção sai a descrição
  oficial: 492 fraudes em 284.807 transações, 0,172%.
- ★ 📄 `DalPozzolo_2014_Learned_Lessons_Credit_Card_Fraud.pdf`: **seção 3.1 (p. 4)**, aprendizado supervisionado
  versus não supervisionado. Justifica o uso de classificação supervisionada.
- ☆ BOLTON; HAND (2002): revisão clássica de detecção estatística de fraude; cite só pela definição do problema.
  https://projecteuclid.org/euclid.ss/1042727940
- ☆ 📄 `DalPozzolo_2018_Realistic_Modeling_TNNLS.pdf`: **seção II (p. 2-4)**, como funciona um sistema real de
  detecção de fraude (camadas de controle, investigadores e *feedback*). Bom para contextualizar.

### 3.2 Desbalanceamento de classes (~30 min)
- ★ HE; GARCIA (2009): referência-padrão sobre dados desbalanceados. Leia **o resumo e a introdução**, suficientes
  para definir o problema e as famílias de soluções (reamostragem e aprendizado sensível ao custo).
  https://doi.org/10.1109/TKDE.2008.239
- ☆ CHAWLA et al. (2002), SMOTE: cite apenas se o grupo explicar por que **não** usou reamostragem sintética.
  Acesso aberto: https://www.jair.org/index.php/jair/article/view/10302
- ☆ 📄 `DalPozzolo_2015_...pdf`: **resumo e seção I (p. 1)**. O *undersampling* distorce as probabilidades
  previstas, o que é mais um motivo para não depender do limiar fixo de 0,5.

### 3.3 Métricas: por que não usar acurácia e por que usar AP (~1 h). **A mais importante**
- ★ 📄 `DalPozzolo_2014_...pdf`: **seção 5 (p. 7-8)**. Trecho citável, com as fórmulas omitidas: "In an
  unbalanced class problem, it is well-known that quantities like TPR [...], TNR [...] and Accuracy [...] are
  misleading assessment measures". Na mesma seção os autores defendem AP e AUC. **Atenção:** as páginas dos
  PDFs desta pasta são as das cópias dos autores, não as da revista. Em citação direta, confira a página na
  versão publicada ou use citação indireta (AUTOR, ano), que dispensa página.
- ★ SAITO; REHMSMEIER (2015): a curva precisão-recall é mais informativa que a ROC em dados desbalanceados, e a
  linha de base da curva PR é a prevalência (≈ 0,0017 neste projeto) e não 0,5. Leia **resumo, introdução e
  conclusão**. Acesso aberto: https://pmc.ncbi.nlm.nih.gov/articles/PMC4349800/
- ★ 📄 `handbook_fraud_detection/4.3_Metricas_sem_limiar_ROC_e_PR.md` (≈ 2 mil palavras): ROC versus PR e AP,
  escrito pelo mesmo grupo que publicou o dataset (ULB).
- ☆ DAVIS; GOADRICH (2006): não se deve interpolar linearmente a curva PR. Justifica usar
  `average_precision_score` em vez de `auc(recall, precisao)`. PDF dos autores:
  https://ftp.cs.wisc.edu/machine-learning/shavlik-group/davis.icml06.pdf
- ☆ 📄 `handbook_fraud_detection/4.2_Metricas_com_limiar.md`: matriz de confusão, precisão, recall e custo.
- ☆ VAN RIJSBERGEN (1979), cap. 7: origem da medida F-beta; β = 2 dá ao recall o dobro do peso da precisão,
  o que justifica o F2. http://www.dcs.gla.ac.uk/Keith/Preface.html

### 3.4 Os três algoritmos (~1 h; em cada um, leia só o resumo e a parte indicada)
| Modelo | Referência principal | O que ler | Complementar |
|---|---|---|---|
| **SGDClassifier** | ★ BOTTOU (2010) | Seções iniciais: a regra de atualização do SGD e por que ele escala para grandes bases. PDF do autor: https://leon.bottou.org/publications/pdf/compstat-2010.pdf | PEDREGOSA et al. (2011) para o scikit-learn |
| **LightGBM** | ★ KE et al. (2017) | Resumo e introdução: histogramas, GOSS e EFB, e por que é rápido. https://proceedings.neurips.cc/paper_files/paper/2017/file/6449f44a102fde848669bdd9eb6b76fa-Paper.pdf | ☆ FRIEDMAN (2001): origem do *gradient boosting* (cite só a ideia) |
| **Rede neural (MLP)** | ★ GOODFELLOW; BENGIO; COURVILLE (2016), **cap. 6, p. 164-167** (introdução de "Deep Feedforward Networks") | Definição de rede *feedforward* e de camadas ocultas. Gratuito: https://www.deeplearningbook.org/contents/mlp.html | RUMELHART; HINTON; WILLIAMS (1986): *backpropagation*; cite sem precisar ler |

- ★ GRINSZTAJN; OYALLON; VAROQUAUX (2022): **resumo e introdução**. Em dados tabulares, modelos de árvore
  costumam superar redes neurais. Isso sustenta a hipótese da comparação (esperar o LightGBM à frente da MLP)
  e dá base para discutir o resultado. Detalhe útil: um dos motivos apontados é que a MLP é invariante a
  rotações, e V1 a V28 **já são uma rotação PCA**.
  https://proceedings.neurips.cc/paper_files/paper/2022/file/0378c7692da36807bdec87ab043cdadc-Paper-Datasets_and_Benchmarks.pdf
- ☆ SHWARTZ-ZIV; ARMON (2022): mesma conclusão (XGBoost versus redes profundas). https://arxiv.org/abs/2106.03253
- ☆ GÉRON (2021), *Mãos à obra* (em português, Alta Books): bom para entender SGD, classificação e MLP se alguém
  do grupo tiver o livro. Os números de capítulo e página da edição brasileira não foram conferidos **[confira]**.

### 3.5 Trabalhos relacionados que usaram ESTE dataset (~45 min; leia só os resumos)
Use-os para mostrar o estado da arte **e** a lacuna: a maioria reporta acurácia, o que infla o resultado.

| Trabalho | Achado | Métrica |
|---|---|---|
| ★ TAHA; MALEBARY (2020) | LightGBM otimizado com busca bayesiana | Acurácia de 98,40% com F1 de só 56,95%: ótimo exemplo do "paradoxo da acurácia" (números do resumo) |
| ★ LEEVY; HANCOCK; KHOSHGOFTAAR (2023), acesso aberto | Classificadores binários (CatBoost, XGBoost, RF, LR) versus de uma classe | Defendem explicitamente a AUPRC |
| ★ HAYAT; MAGNIER (2025), acesso aberto | Crítica metodológica da área: vazamento de dados (reamostrar antes da divisão), falta de validação temporal, recall inflado | Cite na Metodologia para justificar as suas escolhas |
| ☆ MAKKI et al. (2019) | Abordagens para dados desbalanceados com validação estratificada | Reporta AUPRC |
| ☆ AWOYEMI; ADETUNMBI; OLUWADARE (2017) | NB, KNN e regressão logística com reamostragem | Centrado em acurácia |
| ☆ ALARFAJ et al. (2022) | ML clássico e *deep learning* | Centrado em acurácia; números não conferidos **[confira]** |
| ☆ VARMEDJA et al. (2019) | LR, RF, NB e MLP com SMOTE | Centrado em acurácia |

**Em português (bom para a banca da UNIVESP):**
- ★ NICOLA; LAURETTO; DELGADO (2020), ENIAC/SBC, EACH-USP: compara 5 classificadores e 5 métodos de
  balanceamento **neste mesmo dataset**. https://sol.sbc.org.br/index.php/eniac/article/view/12118
- ★ SOUZA; BORDIN JÚNIOR (2023), *Revista Brasileira de Computação Aplicada*: tutorial com o mesmo dataset.
  https://ojs.upf.br/index.php/rbca/article/view/13790

---

## 4. Metodologia (dia 3, ~2 h)

### 4.1 Estrutura exigida pela UNIVESP ("Ouvir, Criar, Implementar")
A tríade vem do *Human Centered Design* da IDEO (em inglês, *Hear / Create / Deliver*).
- ★ IDEO, **HCD – Kit de Ferramentas** (em português): leia só **a introdução das três etapas**.
  https://hcd-connect-production.s3.amazonaws.com/toolkit/en/portuguese_download/ideo_hcd_toolkit_complete_portuguese.pdf
- ★ UNIVESP, *Regulamento para o Projeto Integrador* (2023):
  https://apps.univesp.br/manual-do-aluno/assets/docs/Regulamento_para_o_Projeto_Integrador_jun_2023.pdf
- ☆ GARBIN et al. (2017): artigo de autores da UNIVESP que descreve o método do PI.
  http://www.abed.org.br/congresso2017/trabalhos/pdf/468.pdf
- ☆ CRISP-DM (CHAPMAN et al., 2000; WIRTH; HIPP, 2000): processo-padrão de mineração de dados (entendimento do
  negócio, entendimento dos dados, preparação, modelagem, avaliação, implantação). Encaixa bem dentro do
  "Criar/Implementar". https://www.kde.cs.uni-kassel.de/lehre/ws2012-13/kdd/files/CRISPWP-0800.pdf

### 4.2 Cada decisão do projeto e a referência que a sustenta
As decisões estão documentadas em `analise_exploratoria.ipynb` (seções 1 a 8) e no `README.md`. Use esta tabela
para citar a base de cada uma.

| Decisão no projeto | Por que (fonte) |
|---|---|
| Análise exploratória antes da modelagem; regra do IQR (1,5 × IQR) para diagnosticar outliers | TUKEY (1977) |
| **Manter os outliers** (nas V's eles são o próprio sinal de fraude) | CHANDOLA; BANERJEE; KUMAR (2009): fraude tratada como anomalia |
| Remover duplicatas **antes** da divisão; escalonar dentro do `Pipeline` ajustado só no treino | KAUFMAN et al. (2012): vazamento de dados; HAYAT; MAGNIER (2025) |
| Partição estratificada 80/20 salva; conjunto de teste usado uma única vez | 📄 `handbook_fraud_detection/5.2_Estrategias_de_validacao.md` |
| **AP** como métrica principal; ROC-AUC secundária; acurácia descartada | SAITO; REHMSMEIER (2015); DAL POZZOLO et al. (2014, seção 5); DAVIS; GOADRICH (2006) |
| Limiar por **F2** nas previsões *out-of-fold*, nunca 0,5 fixo | VAN RIJSBERGEN (1979); ELKAN (2001): limiar a partir de custos; DAL POZZOLO et al. (2015, seção IV, p. 4) |
| Validação cruzada estratificada repetida (5 × 3) + **teste t corrigido de Nadeau-Bengio** | NADEAU; BENGIO (2003); BOUCKAERT; FRANK (2004), a versão para *k-fold* repetido; DIETTERICH (1998), por que o teste t comum erra |
| **Correção de Holm** para várias comparações | HOLM (1979) |
| **Intervalo bootstrap** da AP no teste | EFRON; TIBSHIRANI (1993), cap. 13 (intervalos por percentis, p. 168-177) |
| Partição temporal como verificação de robustez (fraudes em rajadas) | DAL POZZOLO et al. (2018), seção VI-D (*concept drift*, p. 10); handbook 5.2 (validação *prequential*) |
| Ferramentas: scikit-learn e LightGBM | PEDREGOSA et al. (2011); KE et al. (2017) |
| Tempo de treino e de inferência na mesma máquina | KE et al. (2017), cuja motivação é a eficiência |

- ☆ Exemplo oficial do scikit-learn que implementa o teste t corrigido (útil para o notebook):
  https://scikit-learn.org/0.24/auto_examples/model_selection/plot_grid_search_stats.html

---

## 5. Plano de leitura em 3 dias

| Dia | Seções do relatório | Ler (★) | Tempo |
|---|---|---|---|
| 1 | Introdução, 2.1 Objetivos, 2.2 Justificativa e delimitação | Tabela da seção 1; Dal Pozzolo 2014 (p. 2-5); Cherif 2023 (resumo) | ~2 h |
| 2 | 2.3 Fundamentação teórica | Dal Pozzolo 2015 (p. 6); Dal Pozzolo 2014 (seção 5, p. 7-8); Saito 2015; handbook 4.3; He & Garcia (resumo); Bottou, Ke, Goodfellow cap. 6 (resumo e introdução); Grinsztajn (resumo); Taha, Leevy, Hayat, Nicola (resumos) | ~4 h |
| 3 | 2.4 Metodologia (+ 2.5 com os notebooks) | IDEO HCD Kit; Regulamento UNIVESP; handbook 5.2; tabela 4.2 | ~2 h |

---

## 6. Arquivos nesta pasta

| Arquivo | O que é | Onde ler |
|---|---|---|
| 📄 `DalPozzolo_2015_Calibrating_Probability_Undersampling.pdf` | Artigo-fonte do dataset (cópia dos autores, 8 p.) | p. 6 (dataset); p. 4-5 (limiar e métricas) |
| 📄 `DalPozzolo_2014_Learned_Lessons_Credit_Card_Fraud.pdf` | Lições práticas de detecção de fraude (versão dos autores, 32 p.) | p. 2-5 (problema); p. 7-8 (métricas) |
| 📄 `DalPozzolo_2018_Realistic_Modeling_TNNLS.pdf` | Modelagem realista de fraude (versão dos autores, 14 p.) | p. 2-5 (sistema real e métricas); p. 10 (*concept drift*) |
| 📄 `handbook_fraud_detection/4.3_Metricas_sem_limiar_ROC_e_PR.md` | ROC, PR e AP (texto do *Handbook* da ULB, CC BY-SA 4.0) | inteiro |
| 📄 `handbook_fraud_detection/4.2_Metricas_com_limiar.md` | Matriz de confusão, precisão, recall e custo | ☆ |
| 📄 `handbook_fraud_detection/5.2_Estrategias_de_validacao.md` | *Hold-out*, *hold-out* repetido, validação *prequential* | inteiro |

Os demais artigos não puderam ser baixados neste ambiente (a rede bloqueia as editoras); os links acima levam às
versões gratuitas quando existem.

---

## 7. Referências (ABNT NBR 6023:2018), em ordem alfabética

Copie só as que efetivamente citar no texto.

ABDALLAH, A.; MAAROF, M. A.; ZAINAL, A. Fraud detection system: a survey. **Journal of Network and Computer Applications**, [*S. l.*], v. 68, p. 90-113, 2016. DOI: https://doi.org/10.1016/j.jnca.2016.04.007.

ALARFAJ, F. K.; MALIK, I.; KHAN, H. U.; ALMUSALLAM, N.; RAMZAN, M.; AHMED, M. Credit card fraud detection using state-of-the-art machine learning and deep learning algorithms. **IEEE Access**, [*S. l.*], v. 10, p. 39700-39715, 2022. DOI: https://doi.org/10.1109/ACCESS.2022.3166891.

ASSOCIAÇÃO BRASILEIRA DAS EMPRESAS DE CARTÕES DE CRÉDITO E SERVIÇOS (ABECS). Pagamentos com cartões atingem a marca de R$ 4,5 trilhões em 2025, crescimento de 10,1%. **Panorama Abecs**, São Paulo, fev. 2026. Disponível em: https://panoramaabecs.com.br/economia-pagamentos-cartoes-brasil-2025-dados-abecs/. Acesso em: 28 set. 2026.

AWOYEMI, J. O.; ADETUNMBI, A. O.; OLUWADARE, S. A. Credit card fraud detection using machine learning techniques: a comparative analysis. *In*: INTERNATIONAL CONFERENCE ON COMPUTING NETWORKING AND INFORMATICS (ICCNI), 2017, Lagos. **Proceedings** [...]. [*S. l.*]: IEEE, 2017. DOI: https://doi.org/10.1109/ICCNI.2017.8123782. [confira as páginas]

BOLTON, R. J.; HAND, D. J. Statistical fraud detection: a review. **Statistical Science**, [*S. l.*], v. 17, n. 3, p. 235-255, 2002. DOI: https://doi.org/10.1214/ss/1042727940.

BOTTOU, L. Large-scale machine learning with stochastic gradient descent. *In*: INTERNATIONAL CONFERENCE ON COMPUTATIONAL STATISTICS (COMPSTAT), 19., 2010, Paris. **Proceedings** [...]. Heidelberg: Physica-Verlag, 2010. p. 177-186. DOI: https://doi.org/10.1007/978-3-7908-2604-3_16.

BOUCKAERT, R. R.; FRANK, E. Evaluating the replicability of significance tests for comparing learning algorithms. *In*: PACIFIC-ASIA CONFERENCE ON KNOWLEDGE DISCOVERY AND DATA MINING (PAKDD), 2004, Sydney. **Advances in Knowledge Discovery and Data Mining**. Berlin: Springer, 2004. (Lecture Notes in Computer Science, v. 3056). p. 3-12. DOI: https://doi.org/10.1007/978-3-540-24775-3_3.

BRASIL. **Lei nº 13.709, de 14 de agosto de 2018**. Lei Geral de Proteção de Dados Pessoais (LGPD). Brasília, DF: Presidência da República, 2018. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm. Acesso em: 28 set. 2026.

BANCO CENTRAL DO BRASIL; CONSELHO MONETÁRIO NACIONAL. **Resolução Conjunta nº 6, de 23 de maio de 2023**. Dispõe sobre requisitos para compartilhamento de dados e informações sobre indícios de fraudes. Brasília, DF: BCB, 2023. Disponível em: https://www.legisweb.com.br/legislacao/?id=445771. Acesso em: 28 set. 2026. [prefira o link oficial do BCB, se abrir]

CHANDOLA, V.; BANERJEE, A.; KUMAR, V. Anomaly detection: a survey. **ACM Computing Surveys**, New York, v. 41, n. 3, art. 15, 2009. DOI: https://doi.org/10.1145/1541880.1541882.

CHAPMAN, P.; CLINTON, J.; KERBER, R.; KHABAZA, T.; REINARTZ, T.; SHEARER, C.; WIRTH, R. **CRISP-DM 1.0**: step-by-step data mining guide. [*S. l.*]: SPSS, 2000. Disponível em: https://www.kde.cs.uni-kassel.de/lehre/ws2012-13/kdd/files/CRISPWP-0800.pdf. Acesso em: 28 set. 2026.

CHAWLA, N. V.; BOWYER, K. W.; HALL, L. O.; KEGELMEYER, W. P. SMOTE: synthetic minority over-sampling technique. **Journal of Artificial Intelligence Research**, [*S. l.*], v. 16, p. 321-357, 2002. DOI: https://doi.org/10.1613/jair.953.

CHERIF, A.; BADHIB, A.; AMMAR, H.; ALSHEHRI, S.; KALKATAWI, M.; IMINE, A. Credit card fraud detection in the era of disruptive technologies: a systematic review. **Journal of King Saud University – Computer and Information Sciences**, [*S. l.*], v. 35, n. 1, p. 145-174, 2023. DOI: https://doi.org/10.1016/j.jksuci.2022.11.008.

DAL POZZOLO, A.; BORACCHI, G.; CAELEN, O.; ALIPPI, C.; BONTEMPI, G. Credit card fraud detection: a realistic modeling and a novel learning strategy. **IEEE Transactions on Neural Networks and Learning Systems**, [*S. l.*], v. 29, n. 8, p. 3784-3797, 2018. DOI: https://doi.org/10.1109/TNNLS.2017.2736643.

DAL POZZOLO, A.; CAELEN, O.; JOHNSON, R. A.; BONTEMPI, G. Calibrating probability with undersampling for unbalanced classification. *In*: IEEE SYMPOSIUM SERIES ON COMPUTATIONAL INTELLIGENCE (SSCI), 2015, Cape Town. **Proceedings** [...]. [*S. l.*]: IEEE, 2015. p. 159-166. DOI: https://doi.org/10.1109/SSCI.2015.33.

DAL POZZOLO, A.; CAELEN, O.; LE BORGNE, Y.-A.; WATERSCHOOT, S.; BONTEMPI, G. Learned lessons in credit card fraud detection from a practitioner perspective. **Expert Systems with Applications**, [*S. l.*], v. 41, n. 10, p. 4915-4928, 2014. Disponível em: https://www.sciencedirect.com/science/article/pii/S095741741400089X. Acesso em: 28 set. 2026. [DOI provável: 10.1016/j.eswa.2014.02.026, confira]

DAVIS, J.; GOADRICH, M. The relationship between precision-recall and ROC curves. *In*: INTERNATIONAL CONFERENCE ON MACHINE LEARNING (ICML), 23., 2006, Pittsburgh. **Proceedings** [...]. New York: ACM, 2006. p. 233-240. DOI: https://doi.org/10.1145/1143844.1143874.

DIETTERICH, T. G. Approximate statistical tests for comparing supervised classification learning algorithms. **Neural Computation**, Cambridge, MA, v. 10, n. 7, p. 1895-1923, 1998. DOI: https://doi.org/10.1162/089976698300017197.

EFRON, B.; TIBSHIRANI, R. J. **An introduction to the bootstrap**. New York: Chapman & Hall, 1993.

ELKAN, C. The foundations of cost-sensitive learning. *In*: INTERNATIONAL JOINT CONFERENCE ON ARTIFICIAL INTELLIGENCE (IJCAI), 17., 2001, Seattle. **Proceedings** [...]. San Francisco: Morgan Kaufmann, 2001. v. 2, p. 973-978.

EUROPEAN BANKING AUTHORITY; EUROPEAN CENTRAL BANK. **2025 report on payment fraud**. Paris; Frankfurt am Main: EBA; ECB, dez. 2025. Disponível em: https://www.ecb.europa.eu/press/intro/publications/pdf/ecb.ebaecb202512.en.pdf. Acesso em: 28 set. 2026.

FEDERAÇÃO BRASILEIRA DE BANCOS (FEBRABAN). **Pesquisa Febraban de Tecnologia Bancária 2026**: vol. 1 – versão executiva. São Paulo: Febraban; Deloitte, jun. 2026. Disponível em: https://cmsarquivos.febraban.org.br/Arquivos/documentos/PDF/Pesquisa%20Febraban%202026.pdf. Acesso em: 28 set. 2026.

FÓRUM BRASILEIRO DE SEGURANÇA PÚBLICA (FBSP). **Anuário Brasileiro de Segurança Pública 2026**. São Paulo: FBSP, 2026. Disponível em: https://forumseguranca.org.br/wp-content/uploads/2026/07/anuario-2026.pdf. Acesso em: 28 set. 2026.

FRIEDMAN, J. H. Greedy function approximation: a gradient boosting machine. **The Annals of Statistics**, [*S. l.*], v. 29, n. 5, p. 1189-1232, 2001. DOI: https://doi.org/10.1214/aos/1013203451.

GARBIN, M. C.; CAVALCANTI, C. C.; LOYOLLA, W.; ARAÚJO, U. F. Prototipagem como estratégia de aprendizagem ativa em cursos de graduação. *In*: CONGRESSO INTERNACIONAL ABED DE EDUCAÇÃO A DISTÂNCIA, 23., 2017, Foz do Iguaçu. **Anais** [...]. São Paulo: ABED, 2017. Disponível em: http://www.abed.org.br/congresso2017/trabalhos/pdf/468.pdf. Acesso em: 28 set. 2026.

GÉRON, A. **Mãos à obra**: aprendizado de máquina com Scikit-Learn, Keras & TensorFlow: conceitos, ferramentas e técnicas para a construção de sistemas inteligentes. 2. ed. Rio de Janeiro: Alta Books, 2021. [a 3. ed. saiu em 2025; cite a edição que usar]

GOODFELLOW, I.; BENGIO, Y.; COURVILLE, A. **Deep learning**. Cambridge, MA: MIT Press, 2016. Disponível em: https://www.deeplearningbook.org/. Acesso em: 28 set. 2026.

GRINSZTAJN, L.; OYALLON, E.; VAROQUAUX, G. Why do tree-based models still outperform deep learning on typical tabular data? *In*: ADVANCES IN NEURAL INFORMATION PROCESSING SYSTEMS (NeurIPS), 35., 2022, New Orleans. **Proceedings** [...]. [*S. l.*]: Curran Associates, 2022. p. 507-520. Datasets and Benchmarks Track.

HAYAT, K.; MAGNIER, B. Data leakage and deceptive performance: a critical examination of credit card fraud detection methodologies. **Mathematics**, Basel, v. 13, n. 16, art. 2563, 2025. DOI: https://doi.org/10.3390/math13162563.

HE, H.; GARCIA, E. A. Learning from imbalanced data. **IEEE Transactions on Knowledge and Data Engineering**, [*S. l.*], v. 21, n. 9, p. 1263-1284, 2009. DOI: https://doi.org/10.1109/TKDE.2008.239.

HOLM, S. A simple sequentially rejective multiple test procedure. **Scandinavian Journal of Statistics**, [*S. l.*], v. 6, n. 2, p. 65-70, 1979.

IDEO. **HCD – Human Centered Design**: kit de ferramentas. 2. ed. [*S. l.*]: IDEO, [2009?]. Disponível em: https://hcd-connect-production.s3.amazonaws.com/toolkit/en/portuguese_download/ideo_hcd_toolkit_complete_portuguese.pdf. Acesso em: 28 set. 2026.

KAUFMAN, S.; ROSSET, S.; PERLICH, C.; STITELMAN, O. Leakage in data mining: formulation, detection, and avoidance. **ACM Transactions on Knowledge Discovery from Data**, New York, v. 6, n. 4, art. 15, p. 1-21, 2012. DOI: https://doi.org/10.1145/2382577.2382579.

KE, G.; MENG, Q.; FINLEY, T.; WANG, T.; CHEN, W.; MA, W.; YE, Q.; LIU, T.-Y. LightGBM: a highly efficient gradient boosting decision tree. *In*: ADVANCES IN NEURAL INFORMATION PROCESSING SYSTEMS (NIPS), 30., 2017, Long Beach. **Proceedings** [...]. [*S. l.*]: Curran Associates, 2017. p. 3146-3154.

LE BORGNE, Y.-A.; SIBLINI, W.; LEBICHOT, B.; BONTEMPI, G. **Reproducible machine learning for credit card fraud detection**: practical handbook. Bruxelas: Université Libre de Bruxelles, 2022. Disponível em: https://fraud-detection-handbook.github.io/fraud-detection-handbook/. Acesso em: 28 set. 2026.

LEEVY, J. L.; HANCOCK, J.; KHOSHGOFTAAR, T. M. Comparative analysis of binary and one-class classification techniques for credit card fraud data. **Journal of Big Data**, [*S. l.*], v. 10, art. 118, 2023. DOI: https://doi.org/10.1186/s40537-023-00794-5.

MAKKI, S.; ASSAGHIR, Z.; TAHER, Y.; HAQUE, R.; HACID, M.-S.; ZEINEDDINE, H. An experimental study with imbalanced classification approaches for credit card fraud detection. **IEEE Access**, [*S. l.*], v. 7, p. 93010-93022, 2019. DOI: https://doi.org/10.1109/ACCESS.2019.2927266.

NADEAU, C.; BENGIO, Y. Inference for the generalization error. **Machine Learning**, [*S. l.*], v. 52, n. 3, p. 239-281, 2003. DOI: https://doi.org/10.1023/A:1024068626366.

NICOLA, V.; LAURETTO, M.; DELGADO, K. V. Avaliação empírica de classificadores e métodos de balanceamento para detecção de fraudes em transações com cartões de créditos. *In*: ENCONTRO NACIONAL DE INTELIGÊNCIA ARTIFICIAL E COMPUTACIONAL (ENIAC), 17., 2020, Evento Online. **Anais** [...]. Porto Alegre: Sociedade Brasileira de Computação, 2020. p. 70-81. DOI: https://doi.org/10.5753/eniac.2020.12118.

NILSON REPORT. **Global card fraud losses at $33 billion**. [*S. l.*]: GlobeNewswire, 7 jan. 2026. Disponível em: https://www.globenewswire.com/news-release/2026/01/07/3214821/0/en/global-card-fraud-losses-at-33-billion.html. Acesso em: 28 set. 2026.

PEDREGOSA, F. *et al*. Scikit-learn: machine learning in Python. **Journal of Machine Learning Research**, [*S. l.*], v. 12, p. 2825-2830, 2011. Disponível em: https://jmlr.org/papers/v12/pedregosa11a.html. Acesso em: 28 set. 2026.

PODER360. Golpes causaram prejuízo de R$ 10,1 bi em 2024, diz Febraban. **Poder360**, Brasília, 12 mar. 2025. Disponível em: https://www.poder360.com.br/poder-economia/golpes-causaram-prejuizo-de-r-101-bi-em-2024-diz-febraban/. Acesso em: 28 set. 2026.

RUMELHART, D. E.; HINTON, G. E.; WILLIAMS, R. J. Learning representations by back-propagating errors. **Nature**, London, v. 323, n. 6088, p. 533-536, 1986. DOI: https://doi.org/10.1038/323533a0.

SAITO, T.; REHMSMEIER, M. The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. **PLoS ONE**, [*S. l.*], v. 10, n. 3, e0118432, 2015. DOI: https://doi.org/10.1371/journal.pone.0118432.

SERASA EXPERIAN. **Tentativas de fraudes bancárias cresceram 10,4% em 2024 e poderiam gerar prejuízo de até R$ 51,6 bilhões, revela Serasa Experian**. São Paulo, mar. 2025. Disponível em: https://www.serasaexperian.com.br/sala-de-imprensa/prevencao-a-fraude/tentativas-de-fraudes-bancarias-cresceram-104-em-2024-e-poderiam-gerar-prejuizo-de-ate-r-516-bilhoes-revela-serasa-experian/. Acesso em: 28 set. 2026.

SHWARTZ-ZIV, R.; ARMON, A. Tabular data: deep learning is not all you need. **Information Fusion**, [*S. l.*], v. 81, p. 84-90, 2022. DOI: https://doi.org/10.1016/j.inffus.2021.11.011.

SOUZA, D. H. M.; BORDIN JÚNIOR, C. J. Detecção de fraude de cartão de crédito por meio de algoritmos de aprendizado de máquina. **Revista Brasileira de Computação Aplicada**, Passo Fundo, v. 15, n. 1, p. 1-11, 2023. DOI: https://doi.org/10.5335/rbca.v15i1.13790.

TAHA, A. A.; MALEBARY, S. J. An intelligent approach to credit card fraud detection using an optimized light gradient boosting machine. **IEEE Access**, [*S. l.*], v. 8, p. 25579-25587, 2020. DOI: https://doi.org/10.1109/ACCESS.2020.2971354.

TUKEY, J. W. **Exploratory data analysis**. Reading, MA: Addison-Wesley, 1977.

UNIVERSIDADE VIRTUAL DO ESTADO DE SÃO PAULO (UNIVESP). **Regulamento para o Projeto Integrador (PI)**. São Paulo: Univesp, jun. 2023. Disponível em: https://apps.univesp.br/manual-do-aluno/assets/docs/Regulamento_para_o_Projeto_Integrador_jun_2023.pdf. Acesso em: 28 set. 2026.

VAN RIJSBERGEN, C. J. **Information retrieval**. 2. ed. London: Butterworths, 1979.

VARMEDJA, D.; KARANOVIC, M.; SLADOJEVIC, S.; ARSENOVIC, M.; ANDERLA, A. Credit card fraud detection: machine learning methods. *In*: INTERNATIONAL SYMPOSIUM INFOTEH-JAHORINA, 18., 2019, East Sarajevo. **Proceedings** [...]. [*S. l.*]: IEEE, 2019. p. 1-5. DOI: https://doi.org/10.1109/INFOTEH.2019.8717766.

WIRTH, R.; HIPP, J. CRISP-DM: towards a standard process model for data mining. *In*: INTERNATIONAL CONFERENCE ON THE PRACTICAL APPLICATIONS OF KNOWLEDGE DISCOVERY AND DATA MINING, 4., 2000, Manchester. **Proceedings** [...]. [*S. l.*: *s. n.*], 2000. p. 29-39. [confira a página final: 39 ou 40]

**Base de dados (cite também):** MACHINE LEARNING GROUP – ULB. **Credit Card Fraud Detection**. [*S. l.*]: Kaggle, 2018. Disponível em: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud. Acesso em: 28 set. 2026. [confira o ano exibido na página do Kaggle]

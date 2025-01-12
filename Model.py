import openai
import time
import datetime

MODEL_NAME = "phi3:mini"

# Configura o client para o Ollama
client = openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="nokeyneeded"
)

class StartupStrategicPlanning:
    def __init__(self, client, model_name, startup_name, mission = "", vision = "", customers = "", startup_stage = "", 
                 value_proposition = "", competitive_advantages = "", performance = 1):
        """
        Inicializa a classe com as informações da startup e configurações do modelo.

        Args:
        - client: Cliente OpenAI configurado.
        - model_name: Nome do modelo a ser usado.
        - startup_name: Nome da startup.
        - Outros campos: Informações sobre a startup.
        - performance: Controle de performance (1 - mínima a 150 - máxima). Default é 1.
        """
        start_time = time.time()

        dt_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.LOG_FILENAME = dt_string + "_" + startup_name + "_execution_log.txt"

        self.client = client
        self.model_name = model_name
        self.startup_info = {
            "startup_name": startup_name,
            "mission": mission,
            "vision": vision,
            "customers": customers,
            "startup_stage": startup_stage,
            "value_proposition": value_proposition,
            "competitive_advantages": competitive_advantages
        }

        self.strategic_objectives = ""

        self.refined_strategic_objectives = ""

        self.missing_informations = [
            key for key, value in self.startup_info.items() if value == ""
        ]
        self.performance = performance

        end_time = time.time()

        # Monta um dicionário de inputs recebidos
        inputs = {
            "client": str(client),
            "model_name": model_name,
            "startup_name": startup_name,
            "mission": mission,
            "vision": vision,
            "customers": customers,
            "startup_stage": startup_stage,
            "value_proposition": value_proposition,
            "competitive_advantages": competitive_advantages,
            "performance": performance
        }

        # Faz o registro no arquivo de log
        self.log_operation(
            function_name="__init__",
            inputs = inputs,
            results = "Classe inicializada",
            start_time = start_time,
            end_time = end_time
        )

    def format_dict_as_table(self, d: dict, sep = "\n") -> str:
        """
        Converte o dicionário em uma tabela de linhas "chave | valor".
        """
        lines = []
        for k, v in d.items():
            lines.append(f"{k} | {v}")
        return sep.join(lines)
    
    def log_operation(self, function_name, inputs, results, start_time, end_time):
        """
        Lê o arquivo de log (se existir), e adiciona uma nova entrada
        contendo dados da execução.
        """
        # Lê o conteúdo anterior do log (somente para exemplificar a leitura)
        try:
            with open(self.LOG_FILENAME, "r", encoding="utf-8") as f:
                previous_logs = f.read()
        except FileNotFoundError:
            previous_logs = ""

        # Formata data/hora e tempo de execução
        dt_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_time = end_time - start_time

        # Converte o startup_info em "tabela"
        info_table = self.format_dict_as_table(self.startup_info)

        # Monta o texto de log
        new_log_entry = (
            f"\n-----\n"
            f"Data/Hora: {dt_string}\n"
            f"Operação: {function_name}\n"
            f"Inputs: {inputs}\n"
            f"Result: {results}\n"
            f"Tempo de execução (s): {total_time:.4f}\n"
            f"Status final de startup_info:\n{info_table}\n"
            f"-----\n"
        )

        # Abre o arquivo em modo append e escreve o novo log
        with open(self.LOG_FILENAME, "a", encoding="utf-8") as f:
            f.write(new_log_entry)

    def get_startup_info(self):
        """Retorna as informações atuais da startup."""
        return self.startup_info

    def get_max_tokens(self): #Max tokens - default: 32064 tokens
        """Calcula o limite de tokens com base na performance."""
        max_t = 200 + (self.performance - 1) * 200 # 200 para performance 1, até 30000 para performance 150
        return max_t
        
    def get_definition(self, target):
        """Retorna a definição clara e concisa de um conceito utilizado."""
        dict_definitions = {
            "startup_name" : "Um nome comercial competitivo, que ganhe destaque no mercado.",
            "mission": "A missão define o propósito principal da startup, ou seja, o que ela faz e para quem.",
            "vision": "A visão é uma representação objetiva do futuro esperado para a startup.",
            "customers": "Os clientes representam o público-alvo ou mercado para o qual a startup oferece seus produtos ou serviços.",
            "startup_stage": "O estágio da startup refere-se à fase do negócio, podendo ser, em ordem de evolução da startup: Ideação, Validação, Operação, Tração ou Scale-Up.",
            "value_proposition": "As propostas de valor são os benefícios entregues pela empresa sob a ótica do cliente, o que agrega valor ao serviço ou produto entregue ao cliente.",
            "competitive_advantages": "As vantagens competitivas são os diferenciais que destacam a startup frente aos concorrentes no mercado.",
        }
        definition = dict_definitions.get(target, "Definição não encontrada. Utilize seu entendimento sobre o termo.")

        return definition

    def model_predict(self, prompt):
        """Instancia o modelo para processar o prompt."""
        messages = [
            {"role": "system", "content": "Você é um assistente de planejamento estratégico para uma startup. Você responde sempre de maneira objetiva e em língua portuguesa."},
            {"role": "user", "content": prompt}
        ]
        response_text = None

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=self.get_max_tokens(),
                temperature=0.05
            )
            response_text = response.choices[0].message.content
        except Exception as e:
            response_text = None

        return response_text

    def fill_informations(self):
        """Preenche campos faltantes utilizando o modelo."""
        start_time = time.time()
        
        for key, value in self.startup_info.items():
            if value == "":
                prompt = f"""Aqui estão as informações atuais da startup: {self.format_dict_as_table(self.startup_info, sep = ",")}""" + \
                f"""\nConsidere que a definição para o campo "{key}" é: {self.get_definition(key)}""" + \
                f"""\nPreciso que você forneça uma resposta objetiva que possa ser usada no campo "{key}"."""
                
                response = self.model_predict(prompt)

                self.startup_info[key] = response

        end_time = time.time()
        
        self.log_operation(
            function_name="fill_informations",
            inputs={},
            results=self.format_dict_as_table(self.startup_info),
            start_time=start_time,
            end_time=end_time
        )

    def response_quality_control(self, include_original_responses = True):
        """Revisa e aprimora respostas dadas pelo modelo."""
        start_time = time.time()

        if include_original_responses: # Se permite a alteração dos dados originalmente fornecidos ou não
            verify_keys = list(self.startup_info.keys())
        else:
            verify_keys = self.missing_informations
            
        for key in verify_keys:
            prompt = f"""Aqui estão as informações atuais da startup: {self.format_dict_as_table(self.startup_info, sep = ",")}""" + \
            f"""\nA resposta sugerida para o campo {key} foi: {self.startup_info[key]}""" + \
            f"""\nRevise e resuma a descrição da resposta, elimine informações desconexas ou inapropriadas.""" + \
            f"""\nRetorne apenas a versão final do texto para ser utilizado no campo '{key}'."""

            response = self.model_predict(prompt)

            if response:
                self.startup_info[key] = response

        end_time = time.time()
        
        self.log_operation(
            function_name="response_quality_control",
            inputs={"include_original_responses" : include_original_responses},
            results=self.format_dict_as_table(self.startup_info),
            start_time=start_time,
            end_time=end_time
        )

    def review_specific_response(self, key):
        """Revisa e aprimora uma resposta específica."""
        raw_response = self.startup_info[key]
        start_time = time.time()
        prompt = f"""Aqui estão as informações atuais da startup: {self.format_dict_as_table(self.startup_info, sep = ",")}""" + \
        f"""\nA resposta sugerida para o campo {key} foi: {self.startup_info[key]}""" + \
        f"""\nRevise e resuma a descrição da resposta, elimine informações desconexas ou inapropriadas.""" + \
        f"""\nRetorne apenas a versão final do texto para ser utilizado no campo '{key}'."""
        
        refined_response = self.model_predict(prompt)
        end_time = time.time()

        if refined_response:
                self.startup_info[key] = refined_response

        self.log_operation(
            function_name="review_specific_response",
            inputs={"key": key, "raw_response": raw_response},
            results=refined_response,
            start_time=start_time,
            end_time=end_time
        )

    def review_target_with_comment(self, target, comment = ""):
        """Aprimora um campo específico com base em um comentário adicional."""
        raw_response = self.startup_info[target]
        start_time = time.time()
        prompt = f"""Aqui estão as informações atuais da startup: {self.format_dict_as_table(self.startup_info, sep = ",")}.""" + \
                f"""O campo '{target}' precisa ser melhorado. O seguinte comentário foi feito: '{comment}'.""" + \
                f"""Revise o conteúdo do campo e sugira uma versão aprimorada com base no comentário."""

        response = self.model_predict(prompt)
        if response:
            self.startup_info[target] = response
        end_time = time.time()

        self.log_operation(
            function_name="review_target",
            inputs={"target": target, "raw_response": raw_response, "comment": comment},
            results=response,
            start_time=start_time,
            end_time=end_time
        )

    def generate_strategic_objectives(self):
        """
        Gera objetivos estratégicos a partir de pares de informações (mission/vision,
        customers/startup_stage, value_proposition/competitive_advantages), e depois
        gera um conjunto adicional combinando todas as informações.
        Retorna uma lista de objetivos estratégicos.
        """
        start_time = time.time()
    
        # Definimos os pares que iremos usar
        pairs = [
            ("mission", "vision"),
            ("customers", "startup_stage"),
            ("value_proposition", "competitive_advantages")
        ]
    
        # Este dicionário armazenará as listas de objetivos para cada par
        # e também uma lista combinada no final
        objectives_results = {
            "mission_vision": [],
            "customers_startup_stage": [],
            "value_proposition_competitive_advantages": [],
            "combined_objectives": []
        }
    
        # 1) Gera objetivos estratégicos para cada par
        for pair in pairs:
            infoA, infoB = pair
            contentA = self.startup_info.get(infoA, "")
            contentB = self.startup_info.get(infoB, "")
    
            # Escolhe uma chave para armazenar no dicionário de resultados
            if pair == ("mission", "vision"):
                result_key = "mission_vision"
            elif pair == ("customers", "startup_stage"):
                result_key = "customers_startup_stage"
            else:
                result_key = "value_proposition_competitive_advantages"
    
            # Formata o prompt para o modelo
            prompt = (
                f"Considere as seguintes informações relativas à minha startup:\n"
                f"- {infoA}: {contentA}\n"
                f"- {infoB}: {contentB}\n\n"
                f"Gere uma lista de objetivos estratégicos para a startup considerando estas informações.\n"
                f"Cada objetivo estratégico deverá ser uma descrição curta e clara com base nas informações fornecidas.\n"
                f"Cada item da lista deverá ser separado por ponto e vírgula - caractere ';'."
            )
    
            # Faz a chamada ao modelo
            response = self.model_predict(prompt)
    
            if response:
                objectives_results[result_key] = response
    
        # 2) Gera um novo conjunto de objetivos correlacionando TUDO
        all_info_table = self.format_dict_as_table(self.startup_info, sep=", ")
        combined_prompt = (
            f"Aqui estão todas as informações atuais da startup:\n"
            f"{all_info_table}\n\n"
            f"Agora, gere uma lista de objetivos estratégicos com base nestas informações."
            f"Cada item da lista deverá ser separado por ponto e vírgula - caractere ';'."
        )
    
        combined_response = self.model_predict(combined_prompt)
        if combined_response:
            objectives_results["combined_objectives"] = combined_response

        self.strategic_objectives = objectives_results
        
        end_time = time.time()
    
        # Registra no log
        self.log_operation(
            function_name="generate_strategic_objectives",
            inputs={self.format_dict_as_table(self.startup_info)},
            results=objectives_results,
            start_time=start_time,
            end_time=end_time
        )

    def refine_strategic_objectives(self):
        """
        Unifica as informações de self.strategic_objectives em uma única string,
        mantém cada objetivo estratégico separado por ponto e vírgula,
        e solicita ao modelo que revise cada objetivo de modo a torná-los mais consistentes
        e resumidos. Armazena o resultado em self.refined_strategic_objectives.
        """
        start_time = time.time()
    
        # 1) Une todos os objetivos de self.strategic_objectives num único texto
        #    Cada item (mission_vision, customers_startup_stage, etc.) é, neste momento,
        #    uma string que contém vários objetivos separados por ponto e vírgula.
        #    Precisamos concatenar tudo numa só string.
    
        combined_objectives = []
        for key in self.strategic_objectives:
            # self.strategic_objectives[key] deve ser uma string. 
            # Se for None ou estiver vazia, é ignorada.
            if self.strategic_objectives[key]:
                combined_objectives.append(self.strategic_objectives[key])
    
        # Junta tudo, cada "bloquinho" separado por ponto e vírgula
        # Se preferir, pode juntar com um " ; " para não duplicar ponto e vírgula.
        all_objectives_text = ";".join(combined_objectives)
    
        # 2) Monta o prompt para o modelo, pedindo para revisar e resumir:
        prompt = (
            "Aqui estão os objetivos estratégicos atuais da minha startup, separados por ponto e vírgula:\n"
            f"{all_objectives_text}\n\n"
            "Por favor, revise e torne cada objetivo o mais consistente e resumido possível, "
            "mantendo cada um separado por ponto e vírgula. Retorne o texto final com os objetivos refinados."
        )
    
        response = self.model_predict(prompt)
    
        if response:
            self.refined_strategic_objectives = response.strip()
    
        end_time = time.time()
    
        # Fazendo o log
        self.log_operation(
            function_name="refine_strategic_objectives",
            inputs={"raw_objectives": all_objectives_text},
            results=self.refined_strategic_objectives,
            start_time=start_time,
            end_time=end_time
        )
    
    def priority_objectives(self):
        """
        Analisa os objetivos estratégicos atualmente em self.refined_strategic_objectives
        e elabora um ranking de prioridade, exibindo primeiro os objetivos mais importantes.
        O resultado é retornado como string (cada objetivo separado por ponto e vírgula).
        """
        start_time = time.time()
    
        # Garante que há informações em refined_strategic_objectives
        if not self.refined_strategic_objectives:
            return None
    
        # Traz as informações da startup para o prompt
        startup_info_text = self.format_dict_as_table(self.startup_info, sep=", ")
    
        prompt = (
            f"Aqui estão as informações da minha startup:\n{startup_info_text}\n\n"
            "Aqui está a lista de objetivos estratégicos, separados por ponto e vírgula:\n"
            f"{self.refined_strategic_objectives}\n\n"
            "Por favor, priorize esses objetivos do mais importante ao menos importante, "
            "considerando as informações da startup. Retorne cada objetivo separado por ponto e vírgula. "
            "O primeiro deve ser o mais prioritário."
        )
    
        response = self.model_predict(prompt)
    
        end_time = time.time()
    
        # Log
        self.log_operation(
            function_name="priority_objectives",
            inputs={"refined_strategic_objectives": self.refined_strategic_objectives},
            results=response,
            start_time=start_time,
            end_time=end_time
        )

        if response:
            self.refined_strategic_objectives = response

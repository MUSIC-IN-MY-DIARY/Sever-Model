from openai import OpenAI
import pandas as pd
# openai API

from config.Authentication import Authentication
# Modules

from typing import List, Dict

class Embedding_Chatbot:
    def __init__(self: str) -> str:
        self.client = OpenAI(
            api_key=Authentication().get_token()
        )
        self.model_id = 'text-embedding-3-small'
        self.embedding_model = self.client.embeddings.create
        # 기초 model parts 생성
    def get_embedding(self, text: str) -> Dict[str, List[float]]:
        text = text.replace('\n', ' ')
        return self.embedding_model(
            input = [text],
            model = model
        ).data[0].embedding

    def create_context(self, question: str, df: pd.DataFrame, max_len: int = 1800) -> str:
        q_embedding = self.get_embedding(question)  # Use the class method to get embedding
        # Calculate cosine similarity for each entry in the dataframe
        df['distances'] = df['embedding'].apply(
            lambda x: cosine_similarity(np.array(q_embedding).reshape(1, -1), np.array(x).reshape(1, -1))[0][0])

        cur_len = 0
        context_parts = []
        # Sort entries by distances in descending order and create context from the most relevant entries
        for _, row in df.sort_values('distances', ascending=False).iterrows():
            additional_length = len(
                row['combined'].split()) + 4  # Assume roughly 1 token per word + space for separators
            if cur_len + additional_length > max_len:
                break
            context_parts.append(row['combined'])
            cur_len += additional_length

        return "\n".join(context_parts)

    def answer_question(self, question: str, df: pd.DataFrame, max_len: int = 1800) -> str:
        context = self.create_context(question, df, max_len=max_len)
        # GPT answer
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Answer the question based on the context below, try to explain anyway but if the question can't be answered based on the context, say \"I don't know\"\n\n",

                    },
                    {
                        "role": "user",
                        "content": f"Context: {context}\n\n---\n\nQuestion: {question}, 한국어로 번역해서 대답해"
                    },
                ],
                temperature=0,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            return "I don't know"
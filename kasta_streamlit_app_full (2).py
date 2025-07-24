
import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Kasta AI Бот", layout="wide")
st.title("🤖 Kasta AI бот: Генерація викладки товарів")

uploaded_file = st.file_uploader("Завантаж Excel-файл з товарами", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success(f"📄 Файл містить {len(df)} рядків.")

    if 'articule' in df.columns:
        st.subheader("🔍 Попередній перегляд артикулів:")
        st.dataframe(df[['articule']].head(10))

        # Потрібні колонки для аналітики
        cols_needed = ['_60d_gross_sales_revenue', '_60d_wishlist_user_count', '_60d_page_view_cnt']
        numeric_cols = [col for col in cols_needed if col in df.columns]

        # 🔎 Загальна аналітика по всьому файлу
        st.subheader("📈 Загальна аналітика по всьому файлу")
        for col in numeric_cols:
            st.markdown(f"**{col}**")
            st.write(f"▫️ Середнє: {df[col].mean():,.0f}")
            st.write(f"▫️ Медіана: {df[col].median():,.0f}")
            st.write(f"▫️ Мінімум: {df[col].min():,.0f}")
            st.write(f"▫️ Максимум: {df[col].max():,.0f}")
            st.markdown("---")

        # 📊 Візуалізація: бар-чарт (лише числові колонки)
        try:
            st.bar_chart(df[numeric_cols])
        except:
            st.warning("⚠️ Не вдалося побудувати графік: перевір типи даних у колонках.")

        # 🏆 Відбір топ-100 товарів
        df['score'] = df[numeric_cols].fillna(0).sum(axis=1)
        top100_df = df.sort_values('score', ascending=False).head(100)
        st.subheader("🔥 Топ-100 товарів:")
        st.dataframe(top100_df[['articule'] + numeric_cols])

        # ✍️ Генерація опису
        if st.button("Згенерувати опис для акції"):
            random_articles = random.sample(list(top100_df['articule']), min(5, len(top100_df)))
            st.markdown("📝 **Опис акції:**")
            st.write(
                f"У нашій акції представлені найпопулярніші товари, які обирають наші клієнти!\n"
                f"Ці артикули заслуговують на увагу: {', '.join(map(str, random_articles))}.\n"
                f"Не зволікай — пропозиція обмежена!"
            )

    else:
        st.warning("⚠️ У файлі не знайдено колонку 'articule' 😥")

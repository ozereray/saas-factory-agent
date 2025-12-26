import os
import re
import json
from groq import Groq
from github import Github

# 1. Bağlantıları Kur (GitHub Secrets'tan okur)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
g = Github(os.getenv("MY_GITHUB_TOKEN"))

def generate_saas_content():
    print("🤖 AI (Llama 3) SaaS fikri ve kodu üretiyor...")
    prompt = (
        "Sen dünya klasmanında bir Full-Stack yazılım mühendisisin. Alman otomotiv disiplini ve "
        "küresel teknoloji ekosistemine uygun, yenilikçi bir SaaS fikri üret. "
        "Üreteceğin çözüm; yapay zeka, veri analitiği veya mobilite teknolojilerini içermeli. "
        "Bana sadece şu JSON formatında yanıt ver:\n"
        "{\n"
        "  \"isim\": \"SaaS ismi\",\n"
        "  \"aciklama\": \"Profesyonel ve kısa bir açıklama\",\n"
        "  \"html\": \"Modern, Tailwind CSS (CDN üzerinden) kullanan, karanlık mod (dark mode) destekli, "
        "animasyonlu ve mobil uyumlu tam kapsamlı bir Landing Page HTML kodu.\"\n"
        "}"
    )

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content)

def deploy_to_github(data):
    # Repo ismini temizle
    repo_name = re.sub(r'\W+', '-', data['isim']).lower() + "-platform"
    user = g.get_user()
    
    print(f"🚀 Yeni repo yayına alınıyor: {repo_name}")
    repo = user.create_repo(repo_name, description=data['aciklama'])
    
    # Dosyaları oluştur (Senin vizyonunu temsil eder)
    repo.create_file("index.html", "Initial Landing Page", data['html'])
    repo.create_file("README.md", "Documentation", f"# {data['isim']}\n\n{data['aciklama']}\n\n*Built by OzerEray AI Factory*")
    
    return repo.html_url

if __name__ == "__main__":
    # Try-except kaldırıldı ki hata varsa direkt görelim
    saas_data = generate_saas_content()
    url = deploy_to_github(saas_data)
    print(f"✅ BAŞARILI: {url}")
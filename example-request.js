// Exemplo de como fazer uma requisição para a API

const dadosPaciente = [
  {
    "nome": "Ana Silva",
    "cpf": "123.456.789-00",
    "sexo": "Feminino",
    "faixa_etaria": "25-34",
    "tipo_usuario": "profissional",
    "data_registro": "2025-11-01 10:30:00",
    "data_inicio_sintomas": "2025-10-28",
    "data_avc": "2025-10-29",
    "tipo_avc": "Isquêmico",
    "admissao_janela_terapeutica": "Sim",
    "trombolise": "Sim",
    "trombectomia": "Não",
    "medicamentos_utilizados": "AAS, Clopidogrel",
    "ventilacao_mecanica": "Não",
    "tempo_ventilacao": "",
    "intubado": "Não",
    "traqueostomizado": "Não",
    "sequelas": "Leve déficit motor braço direito",
    "desfecho": "Alta",
    "alta_medicamento": "Sim",
    "alta_medicamento_qual": "AAS",
    "grau_parentesco": "",
    "cuidador_externo": "",
    "tempo_chegada_hospital": "",
    "comorbidades": "Hipertensão",
    "historico_familiar": "Pai com AVC",
    "medicamento_uso_diario": "Sim",
    "medicamento_uso_diario_qual": "Losartana",
    "alimentacao": "Equilibrada",
    "atividade_fisica": "2x/semana",
    "tabagismo": "Não",
    "alcool": "Socialmente",
    "uso_medicamentos": "",
    "uso_medicamentos_qual": ""
  }
];

// Substitua pela URL da sua API no Vercel
const API_URL = 'https://seu-dominio.vercel.app/api/generate-pdf';

async function gerarPDF() {
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(dadosPaciente)
    });

    const data = await response.json();

    if (data.success) {
      console.log('PDFs gerados com sucesso!');
      console.log(`Total: ${data.pdfs.length} PDF(s)`);
      
      // Exemplo: baixar o primeiro PDF
      data.pdfs.forEach((pdf, index) => {
        // Converter base64 para blob
        const byteCharacters = atob(pdf.pdf_base64);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: 'application/pdf' });
        
        // Criar link de download
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = pdf.nome;
        link.click();
        URL.revokeObjectURL(url);
      });
    } else {
      console.error('Erro:', data.error);
    }
  } catch (error) {
    console.error('Erro na requisição:', error);
  }
}

// Chamar a função
gerarPDF();


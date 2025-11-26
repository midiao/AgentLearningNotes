import similarity as np

embedding = {
    "king": np.array([0.9, 0.8]),
    "queen": np.array([0.9, 0.2]),
    "man": np.array([0.7, 0.9]),
    "woman": np.array([0.7, 0.3])
}

def consine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return dot_product / norm_product

result_vec = embedding["king"] - embedding["man"] + embedding["woman"]

sim = consine_similarity(result_vec, embedding["queen"])

print(f"king - man + woman 的结果向量: {result_vec}")
print(f"该结果与'queen'的相似度: {sim:.4f}")
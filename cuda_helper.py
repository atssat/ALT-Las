try:
    import torch
    def is_cuda_available():
        return torch.cuda.is_available()
except ImportError:
    def is_cuda_available():
        return False

if __name__ == "__main__":
    print(f"CUDA Available: {is_cuda_available()}")

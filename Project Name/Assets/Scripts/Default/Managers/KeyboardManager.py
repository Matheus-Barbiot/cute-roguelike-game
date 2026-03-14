#icon=SCRIPTWIN
import bge

class Keyboard:
    def __init__(self):
        self.keyboard = bge.logic.keyboard.inputs
        
        self._num_map = {
            "0": "ZERO", "1": "ONE", "2": "TWO", "3": "THREE", 
            "4": "FOUR", "5": "FIVE", "6": "SIX", "7": "SEVEN", 
            "8": "EIGHT", "9": "NINE"
        }

        self._special_map = {
            "shift": "SHIFTKEY", "ctrl": "CTRLKEY", "alt": "ALTKEY",
            "enter": "ENTERKEY", "esc": "ESCKEY", "space": "SPACEKEY",
            "tab": "TABKEY", "backspace": "BACKSPACEKEY"
        }

    # --- MÉTODOS DE CONVERSÃO INTERNOS ---

    def alpha_key(self, input_string):
        try:
            char = str(input_string)[0].upper()
            return getattr(bge.events, f"{char}KEY")
        except:
            return None

    def number_key(self, input_number, type="key"):
        num_str = str(input_number)[0]
        if num_str in self._num_map:
            const = f"PAD{num_str}" if type == "pad" else f"{self._num_map[num_str]}KEY"
            return getattr(bge.events, const, None)
        return None

    def special_key(self, name, side=None):
        name = name.lower()
        base = self._special_map.get(name)
        if not base: return None
        
        full_name = f"{side.upper()}{base}" if side and side.lower() in ["left", "right"] else \
                    (f"LEFT{base}" if name in ["shift", "ctrl", "alt"] else base)
        return getattr(bge.events, full_name, None)
    
    def arrow_key(self, direction):
        name = f'{direction.upper()}ARROWKEY'
        
        return getattr(bge.events, name, None)
    # --- O CÉREBRO: AUTO-DETECTOR DE INPUT ---

    def _smart_decode(self, raw_input):
        """
        Analisa o tipo de dado enviado e converte para um bge.event válido.
        """
        # 1. Se já for um inteiro (bge.event), retorna ele mesmo
        if isinstance(raw_input, int):
            return raw_input
        
        # 2. Se for uma string
        if isinstance(raw_input, str):
            # Se for uma das teclas especiais mapeadas (shift, ctrl, etc)
            if raw_input.lower() in self._special_map:
                return self.special_key(raw_input)
            
            # Se a string for um número ("1")
            if raw_input.isdigit():
                return self.number_key(raw_input)
            
            # Se for apenas uma letra ("W" ou "A")
            if len(raw_input) >= 1:
                return self.alpha_key(raw_input)
        
        print(f"[KeyboardManager Error]: Não foi possível identificar o input: {raw_input}")
        return None

    # --- FUNÇÕES DE ESTADO COM AUTO-CONVERSÃO ---

    def _get_status(self, raw_input):
        # Converte automaticamente antes de verificar o status
        key_code = self._smart_decode(raw_input)
        
        if key_code and key_code in self.keyboard:
            return self.keyboard[key_code]
        return None

    def active(self, key):
        """Ex: kb.active('W') ou kb.active(bge.events.WKEY) ou kb.active('shift')"""
        status = self._get_status(key)
        return status.active if status else False

    def activated(self, key):
        """Retorna True no frame em que a tecla foi pressionada."""
        status = self._get_status(key)
        return status.activated if status else False

    def released(self, key):
        """Retorna True no frame em que a tecla foi solta."""
        status = self._get_status(key)
        return status.released if status else False

    def value(self, key):
        """Retorna o valor analógico (0.0 a 1.0)."""
        status = self._get_status(key)
        return status.values[-1] if status else 0.0

# Instância Singleton

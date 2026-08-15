/**
 * technibel_ir.h
 * Générateur de trames IR pour climatiseur Technibel SCDF32C5I
 *
 * Protocole reverse-engineered :
 *   48 bits · 38kHz · header 6500µs/3300µs
 *   Bit1 = ~450µs pulse / ~2200µs space
 *   Bit0 = ~450µs pulse / ~900µs space
 *
 * Structure :
 *   B0 = 0xD0  (device address, fixe)
 *   B1 = mode  (COOL=0xAC, DRY=0xAA, FAN=0xA9, AUTO=0xAD)
 *   B2 = (temp_nibble_hi << 4) | fan_nibble_lo
 *          temp_hi = (reverseBits8(consigne-4) >> 4) & 0xF
 *          fan_lo  : AUTO=0x8, FAN_LOW=0xC, FAN_MED=0xE, FAN_HIGH=0xB
 *   B3 = 0x18 (ON) | 0x08 (OFF)
 *   B4 = 0x03  (fixe)
 *   B5 = reverseBits8( lsb(B2) + lsb(B3) + T_amb - 25 )
 */

#pragma once
#include <vector>
#include <cstdint>

// ── Constantes protocole ──────────────────────────────────────────────────────
static const uint16_t TECHNIBEL_HEADER_PULSE  = 6500;
static const uint16_t TECHNIBEL_HEADER_SPACE  = 3300;
static const uint16_t TECHNIBEL_BIT_PULSE     =  450;
static const uint16_t TECHNIBEL_BIT_ONE_SPACE = 2200;
static const uint16_t TECHNIBEL_BIT_ZER_SPACE =  900;

// ── Enums — préfixés pour éviter les conflits avec les macros Arduino ─────────
// (LOW=0x0 et HIGH=0x1 sont définis dans esp32-hal-gpio.h)
enum class TechnibelMode : uint8_t {
  COOL = 0xAC,
  DRY  = 0xAA,
  FAN  = 0xA9,
  AUTO = 0xAD,
};

enum class TechnibelFan : uint8_t {
  FAN_AUTO = 0x8,
  FAN_LOW  = 0xC,
  FAN_MED  = 0xE,
  FAN_HIGH = 0xB,
};

// ── Inversion des bits d'un byte ──────────────────────────────────────────────
static uint8_t technibel_reverse_bits(uint8_t b) {
  uint8_t r = 0;
  for (int i = 0; i < 8; i++) r |= ((b >> i) & 1) << (7 - i);
  return r;
}

// ── Construction de la trame 6 bytes ─────────────────────────────────────────
static std::vector<uint8_t> technibel_build_frame(
    TechnibelMode mode,
    uint8_t consigne,
    TechnibelFan fan,
    bool power,
    uint8_t t_amb
) {
  uint8_t B0 = 0xD0;
  uint8_t B1 = static_cast<uint8_t>(mode);
  uint8_t tempHi = (technibel_reverse_bits(consigne - 4) >> 4) & 0x0F;
  uint8_t fanLo  = static_cast<uint8_t>(fan);
  uint8_t B2 = (tempHi << 4) | fanLo;
  uint8_t B3 = power ? 0x18 : 0x08;
  uint8_t B4 = 0x03;
  uint8_t B5 = technibel_reverse_bits(
    (uint8_t)((technibel_reverse_bits(B2) + technibel_reverse_bits(B3) + t_amb - 25) & 0xFF)
  );
  return {B0, B1, B2, B3, B4, B5};
}

// ── Conversion bytes → séquence RAW IR ───────────────────────────────────────
static std::vector<int32_t> technibel_frame_to_raw(const std::vector<uint8_t>& frame) {
  std::vector<int32_t> raw;
  raw.push_back(TECHNIBEL_HEADER_PULSE);
  raw.push_back(-(int32_t)TECHNIBEL_HEADER_SPACE);
  for (uint8_t byte : frame) {
    for (int i = 7; i >= 0; i--) {
      raw.push_back(TECHNIBEL_BIT_PULSE);
      raw.push_back(((byte >> i) & 1)
        ? -(int32_t)TECHNIBEL_BIT_ONE_SPACE
        : -(int32_t)TECHNIBEL_BIT_ZER_SPACE);
    }
  }
  raw.push_back(TECHNIBEL_BIT_PULSE);
  return raw;
}

// ── Point d'entrée principal ──────────────────────────────────────────────────
static std::vector<int32_t> technibel_build_raw(
    TechnibelMode mode,
    uint8_t consigne,
    TechnibelFan fan,
    bool power,
    uint8_t t_amb
) {
  return technibel_frame_to_raw(technibel_build_frame(mode, consigne, fan, power, t_amb));
}

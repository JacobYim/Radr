#!/bin/bash
# Extreme SSD (exfat, UUID 3AB9-F7B8) → 고정 마운트 /mnt/extreme-ssd
# 사용: SSD 연결 후  sudo bash setup_extreme_ssd_fstab.sh

set -euo pipefail

MOUNT="/mnt/extreme-ssd"
UUID="3AB9-F7B8"
FSTYPE="exfat"
# radr 기본 uid/gid=1000 (다른 사용자면 uid/gid 수정)
OPTS="defaults,nofail,uid=1000,gid=1000,umask=0022"

if [[ "${EUID:-}" -ne 0 ]]; then
  echo "sudo 로 실행하세요: sudo bash $0" >&2
  exit 1
fi

mkdir -p "$MOUNT"

if grep -qF "$UUID" /etc/fstab; then
  echo "/etc/fstab 에 이미 이 UUID 가 있습니다."
else
  echo "UUID=$UUID $MOUNT $FSTYPE $OPTS 0 0" >> /etc/fstab
  echo "/etc/fstab 에 항목을 추가했습니다."
fi

OLD_MP="/media/radr/Extreme SSD"
if mountpoint -q "$OLD_MP" 2>/dev/null; then
  echo "기존 자동 마운트 해제: $OLD_MP"
  umount "$OLD_MP" || true
fi

mount "$MOUNT" 2>/dev/null || mount -a

if mountpoint -q "$MOUNT"; then
  echo "마운트 확인됨: $MOUNT"
  df -h "$MOUNT"
  ls -la "$MOUNT" | head
else
  echo "경고: $MOUNT 가 아직 마운트되지 않았습니다. SSD 연결 후 다시: sudo mount $MOUNT" >&2
  exit 1
fi

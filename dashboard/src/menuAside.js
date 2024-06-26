import {
  mdiMonitor,
  mdiGithub,
  mdiQrcode
} from '@mdi/js'

export default [
  {
    to: '/',
    icon: mdiMonitor,
    label: 'Dashboard'
  },
  {
    to:'/qrcode',
    label: 'QR Code',
    icon: mdiQrcode,
  },
  {
    href: 'https://github.com/vitordwb/prime-dashboard',
    label: 'GitHub',
    icon: mdiGithub,
    target: '_blank'
  },
]

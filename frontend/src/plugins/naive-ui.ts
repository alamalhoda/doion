import { create, lightTheme, darkTheme } from 'naive-ui'

// Naive UI theme override aligned with cheque-marketplace design system
export const lightDesignTheme = create({
  common: {
    primaryColor: '#0C2340',
    primaryColorHover: '#1A3D6B',
    primaryColorPressed: '#0C2340',
    primaryColorSuppl: '#0C2340',
    infoColor: '#2A5FA8',
    successColor: '#0D7A72',
    warningColor: '#D4730A',
    errorColor: '#C0392B',
    bodyColor: '#F5F4F0',
    cardColor: '#FFFFFF',
    modalColor: '#FFFFFF',
    popoverColor: '#FFFFFF',
    tableColor: '#FFFFFF',
    textColor: '#1A1613',
    textColorSecondary: '#4A4540',
    textColorTertiary: '#7A7570',
    dividerColor: '#E0DDD5',
    borderColor: '#E0DDD5',
    borderRadius: '6px',
    borderRadiusLarge: '10px',
  },
  Button: {
    borderRadiusMedium: '6px',
    paddingMedium: '0.6rem 1.6rem',
    paddingSmall: '0.35rem 0.9rem',
    paddingLarge: '0.75rem 2rem',
    fontWeightMedium: '600',
  },
  Input: {
    borderRadius: '6px',
    borderHover: '#2A5FA8',
    borderFocus: '#2A5FA8',
    boxShadowFocus: '0 0 0 2px rgba(42, 95, 168, 0.12)',
  },
  Card: {
    borderRadius: '10px',
    borderColor: '#E0DDD5',
  },
  Tab: {
    borderRadius: '6px',
    paddingMedium: '0.4rem 1rem',
  },
  Select: {
    borderRadius: '6px',
  },
  Modal: {
    borderRadius: '10px',
  },
  DataTable: {
    borderRadius: '10px',
    thColor: '#F8F7F3',
    thTextColor: '#4A4540',
    tdTextColor: '#1A1613',
    tdPaddingMedium: '0.85rem 1.1rem',
    thPaddingMedium: '0.85rem 1.1rem',
  },
  Message: {
    borderRadius: '10px',
  },
  Notification: {
    borderRadius: '10px',
  },
  Tag: {
    borderRadius: '6px',
    paddingMedium: '0.2rem 0.6rem',
    fontSizeSmall: '12px',
    fontSizeMedium: '12px',
  },
})

export const darkDesignTheme = create({
  common: {
    primaryColor: '#EAC84A',
    primaryColorHover: '#F0D675',
    primaryColorPressed: '#C9960A',
    primaryColorSuppl: '#EAC84A',
    infoColor: '#2A5FA8',
    successColor: '#0D7A72',
    warningColor: '#D4730A',
    errorColor: '#C0392B',
    bodyColor: '#0f1419',
    cardColor: '#1a2027',
    modalColor: '#1a2027',
    popoverColor: '#1a2027',
    tableColor: '#1a2027',
    textColor: '#e6edf3',
    textColorSecondary: '#b0b8c4',
    textColorTertiary: '#7d8590',
    dividerColor: '#2d3748',
    borderColor: '#2d3748',
    borderRadius: '6px',
    borderRadiusLarge: '10px',
  },
  Button: {
    borderRadiusMedium: '6px',
    paddingMedium: '0.6rem 1.6rem',
    paddingSmall: '0.35rem 0.9rem',
    paddingLarge: '0.75rem 2rem',
    fontWeightMedium: '600',
  },
  Input: {
    borderRadius: '6px',
    borderHover: '#EAC84A',
    borderFocus: '#EAC84A',
    boxShadowFocus: '0 0 0 2px rgba(234, 200, 74, 0.15)',
  },
  Card: {
    borderRadius: '10px',
    borderColor: '#2d3748',
  },
  Tab: {
    borderRadius: '6px',
    paddingMedium: '0.4rem 1rem',
  },
  Select: {
    borderRadius: '6px',
  },
  Modal: {
    borderRadius: '10px',
  },
  DataTable: {
    borderRadius: '10px',
    thColor: '#232b36',
    thTextColor: '#b0b8c4',
    tdTextColor: '#e6edf3',
    tdPaddingMedium: '0.85rem 1.1rem',
    thPaddingMedium: '0.85rem 1.1rem',
  },
  Message: {
    borderRadius: '10px',
  },
  Notification: {
    borderRadius: '10px',
  },
  Tag: {
    borderRadius: '6px',
    paddingMedium: '0.2rem 0.6rem',
    fontSizeSmall: '12px',
    fontSizeMedium: '12px',
  },
})

export const goldTheme = create({
  common: {
    primaryColor: '#C9960A',
    primaryColorHover: '#EAC84A',
    primaryColorPressed: '#C9960A',
    primaryColorSuppl: '#EAC84A',
  },
})

export default function setupNaiveUI(app: any) {
  app.use(create({
    theme: {
      defaultTheme: 'light',
      themes: {
        light: lightDesignTheme,
        dark: darkDesignTheme,
      },
    },
  }))
}

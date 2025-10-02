import React from 'react';
import type { Metadata } from 'next';
import { ConfigProvider, theme } from 'antd';
import StyledComponentsRegistry from '@/lib/AntdRegistry';
import './globals.css';

export const metadata: Metadata = {
    title: 'SimSXCu - Industrial Simulation Tool',
    description: 'A smart, interactive web-based simulation tool for copper solvent extraction, powered by a robust backend.',
};

// Define the Industrial Dark Theme palette
const industrialDarkTheme = {
    token: {
        colorPrimary: '#3b82f6', // Metallic Blue
        colorInfo: '#3b82f6',
        colorSuccess: '#10b981', // Green
        colorWarning: '#f59e0b', // Orange
        colorError: '#ef4444',
        colorBgBase: '#1f2937', // Main background
        colorBgContainer: '#374151', // Panel background
        colorTextBase: '#e5e7eb',
        colorBorder: '#4b5563',
        borderRadius: 6,
    },
    algorithm: theme.darkAlgorithm,
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body>
                <StyledComponentsRegistry>
                    <ConfigProvider theme={industrialDarkTheme}>
                        {children}
                    </ConfigProvider>
                </StyledComponentsRegistry>
            </body>
        </html>
    );
}

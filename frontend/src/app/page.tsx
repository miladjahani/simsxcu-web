'use client';

import React from 'react';
import { Layout, Typography, Card, Button, Space, Alert } from 'antd';

const { Header, Content } = Layout;
const { Title, Paragraph } = Typography;

export default function HomePage() {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ padding: '0 24px', display: 'flex', alignItems: 'center' }}>
        <Title level={3} style={{ color: 'white', margin: 0 }}>
          SimSXCu - Industrial Simulation Tool
        </Title>
      </Header>
      <Content style={{ padding: '24px 48px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <Card
            title={<Title level={4}>Welcome, Senior Process Engineer</Title>}
            bordered={false}
            style={{ marginBottom: '24px' }}
          >
            <Paragraph>
              This is the central hub for the SimSXCu simulation tool. Our mission is to transform complex spreadsheet calculations into a smart, interactive, and intuitive web-based experience.
            </Paragraph>
            <Paragraph>
              The UI is built with Ant Design and features a custom-built **Industrial Dark Theme** to provide a professional and focused work environment. The color palette has been carefully selected for clarity and reduced eye strain during long analysis sessions.
            </Paragraph>
            <Alert
              message="System Status: Backend API is running. Frontend is rendered. Ready for component implementation."
              type="success"
              showIcon
              style={{ marginBottom: '24px' }}
            />
            <Space size="large">
              <Button type="primary">Primary Action</Button>
              <Button>Default Button</Button>
              <Button type="dashed">Dashed Button</Button>
            </Space>
          </Card>

           <Card title="Theme Color Palette Test">
                <Space wrap>
                    <Button type="primary" style={{backgroundColor: '#3b82f6'}}>Primary (Metallic Blue)</Button>
                    <Button style={{backgroundColor: '#10b981', color: 'white'}}>Success (Green)</Button>
                    <Button style={{backgroundColor: '#f59e0b', color: 'white'}}>Warning (Orange)</Button>
                    <Button danger>Error</Button>
                </Space>
           </Card>

        </div>
      </Content>
    </Layout>
  );
}
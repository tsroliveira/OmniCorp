import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchRoles, createRole, updateRole, deleteRole } from '../store/roleSlice';
import { Table, Button, Modal, Form, Input, Select } from 'antd';

const Roles = () => {
    const dispatch = useDispatch();
    const roles = useSelector((state) => state.roles.items);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [currentRole, setCurrentRole] = useState(null);

    useEffect(() => {
        dispatch(fetchRoles());
    }, [dispatch]);

    const handleCreate = () => {
        setCurrentRole(null);
        setIsModalVisible(true);
    };

    const handleEdit = (role) => {
        setCurrentRole(role);
        setIsModalVisible(true);
    };

    const handleDelete = (roleId) => {
        dispatch(deleteRole(roleId));
    };

    const handleOk = (values) => {
        if (currentRole) {
            dispatch(updateRole({ ...currentRole, ...values }));
        } else {
            dispatch(createRole(values));
        }
        setIsModalVisible(false);
    };

    const handleCancel = () => {
        setIsModalVisible(false);
    };

    const columns = [
        {
            title: 'Nome',
            dataIndex: 'name',
            key: 'name',
        },
        {
            title: 'Descrição',
            dataIndex: 'description',
            key: 'description',
        },
        {
            title: 'Ações',
            key: 'actions',
            render: (text, record) => (
                <>
                    <Button onClick={() => handleEdit(record)}>Editar</Button>
                    <Button onClick={() => handleDelete(record.id)} danger>Excluir</Button>
                </>
            ),
        },
    ];

    return (
        <div>
            <h1>Gerenciamento de Perfis</h1>
            <Button type="primary" onClick={handleCreate}>Novo Perfil</Button>
            <Table columns={columns} dataSource={roles} rowKey="id" />
            <Modal
                title={currentRole ? "Editar Perfil" : "Novo Perfil"}
                visible={isModalVisible}
                onCancel={handleCancel}
                footer={null}
            >
                <Form
                    initialValues={currentRole || { name: '', description: '' }}
                    onFinish={handleOk}
                >
                    <Form.Item
                        name="name"
                        label="Nome"
                        rules={[{ required: true, message: 'Por favor, insira o nome do perfil!' }]}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        name="description"
                        label="Descrição"
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="submit">
                            {currentRole ? "Atualizar" : "Criar"}
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default Roles; 
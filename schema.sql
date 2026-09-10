-- =====================================================
-- SCHÉMA PHARMA-CHATBOT - MVP
-- =====================================================

-- Fonction pour mise à jour automatique de updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ---------- Produits (médicaments) ----------
CREATE TABLE produits (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    prix DECIMAL(10,2) NOT NULL CHECK (prix >= 0),
    categorie VARCHAR(100),
    ordonnance_requise BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_produits_nom ON produits(nom);

-- ---------- Fournisseurs ----------
CREATE TABLE fournisseurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    contact VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    telephone VARCHAR(50),
    adresse TEXT
);

-- ---------- Stock ----------
CREATE TABLE stock (
    id SERIAL PRIMARY KEY,
    produit_id INTEGER REFERENCES produits(id) ON DELETE CASCADE,
    fournisseur_id INTEGER REFERENCES fournisseurs(id) ON DELETE SET NULL,
    quantite INTEGER NOT NULL DEFAULT 0 CHECK (quantite >= 0),
    seuil_alerte INTEGER DEFAULT 10 CHECK (seuil_alerte >= 0),
    date_peremption DATE,
    updated_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_stock_produit ON stock(produit_id);

CREATE TRIGGER stock_updated_at
BEFORE UPDATE ON stock
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- ---------- Alertes ----------
CREATE TABLE alertes (
    id SERIAL PRIMARY KEY,
    produit_id INTEGER REFERENCES produits(id) ON DELETE CASCADE,
    type VARCHAR(50) CHECK (type IN ('epuisement', 'peremption')),
    message TEXT,
    resolue BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_alertes_resolue ON alertes(resolue);

"""
Tests for Poisson regression models.
"""

import pytest
import numpy as np
from sklearn.model_selection import train_test_split

from amgd.models import PoissonRegressor
from amgd.benchmarks.datasets import generate_synthetic_poisson_data


class TestPoissonRegressor:
    """Test Poisson regression implementation."""
    
    @pytest.fixture
    def poisson_data(self):
        """Generate synthetic Poisson data."""
        X, y, true_coef = generate_synthetic_poisson_data(
            n_samples=200,
            n_features=50,
            n_informative=10,
            sparsity=0.8,
            random_state=42
        )
        return X, y, true_coef
        
    def test_poisson_fit_predict(self, poisson_data):
        """Test basic fit and predict."""
        X, y, _ = poisson_data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
        
        model = PoissonRegressor(optimizer='amgd', penalty='none')
        model.fit(X_train, y_train)
        
        # Check that model is fitted
        assert hasattr(model, 'coef_')
        assert hasattr(model, 'intercept_')
        assert model.is_fitted_
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Predictions should be non-negative (Poisson constraint)
        assert np.all(y_pred >= 0)
        
        # Check score method
        score = model.score(X_test, y_test)
        assert isinstance(score, float)
        
    def test_poisson_with_l1_penalty(self, poisson_data):
        """Test Poisson regression with L1 penalty."""
        X, y, true_coef = poisson_data
        
        model = PoissonRegressor(
            optimizer='amgd',
            penalty='l1',
            lambda1=0.1,
            max_iter=500
        )
        model.fit(X, y)
        
        # Check sparsity
        n_nonzero = np.sum(np.abs(model.coef_) > 1e-6)
        sparsity = 1 - n_nonzero / len(model.coef_)
        
        assert sparsity > 0.5  # Should be at least 50% sparse
        
    def test_poisson_with_elasticnet(self, poisson_data):
        """Test Poisson regression with Elastic Net."""
        X, y, _ = poisson_data
        
        model = PoissonRegressor(
            optimizer='amgd',
            penalty='elasticnet',
            lambda1=0.05,
            lambda2=0.05,
            max_iter=500
        )
        model.fit(X, y)
        
        # Should produce some sparsity but less than pure L1
        n_nonzero = np.sum(np.abs(model.coef_) > 1e-6)
        sparsity = 1 - n_nonzero / len(model.coef_)
        
        assert 0.2 < sparsity < 0.8
        
    def test_different_optimizers(self, poisson_data):
        """Test different optimizers produce reasonable results."""
        X, y, _ = poisson_data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
        
        optimizers = ['amgd', 'adam', 'adagrad']
        scores = {}
        
        for opt in optimizers:
            model = PoissonRegressor(optimizer=opt, penalty='l1', lambda1=0.05)
            model.fit(X_train, y_train)
            scores[opt] = model.score(X_test, y_test)
            
        # All optimizers should produce reasonable scores
        for opt, score in scores.items():
            assert score > -10  # Reasonable bound for negative deviance
            
    def test_warm_start(self, poisson_data):
        """Test warm start functionality."""
        X, y, _ = poisson_data
        
        model = PoissonRegressor(
            optimizer='amgd',
            penalty='l1',
            lambda1=0.1,
            warm_start=True,
            max_iter=50
        )
        
        # First fit
        model.fit(X, y)
        coef1 = model.coef_.copy()
        n_iter1 = model.n_iter_
        
        # Second fit with warm start
        model.max_iter = 100
        model.fit(X, y)
        coef2 = model.coef_.copy()
        n_iter2 = model.n_iter_
        
        # Coefficients should change (continued optimization)
        assert not np.allclose(coef1, coef2)
        # Should need fewer iterations due to warm start
        assert n_iter2 <= 50
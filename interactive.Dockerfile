FROM ghcr.io/habecker/tensorflow_poetry:py3.10.11-tf2.12.0-slim

COPY ./ /insurance-prediction

WORKDIR /insurance-prediction

RUN poetry install

RUN echo '#!/bin/bash' > /info.sh
RUN echo "echo ICAgX18gIF9fIF8gICAgIF9fXyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICB8ICBcLyAgfCB8ICAgLyBfIFwgXyBfXyAgX19fICAgICAgICAgICAgICAgICAgICAKICB8IHxcL3wgfCB8ICB8IHwgfCB8ICdfIFwvIF9ffCAgICAgICAgICAgICAgICAgICAKICB8IHwgIHwgfCB8X198IHxffCB8IHxfKSBcX18gXCAgICAgICAgICAgICAgICAgICAKICB8X3wgIHxffF9fX19fXF9fXy98IC5fXy98X19fLyBfICAgICAgICAgICAgICAgICAKICBcIFwgICAgICAvIC9fXyAgXyB8X3wgfCBfX19fX3wgfF9fICAgX19fICBfIF9fICAKICAgXCBcIC9cIC8gLyBfIFx8ICdfX3wgfC8gLyBfX3wgJ18gXCAvIF8gXHwgJ18gXCAKICAgIFwgViAgViAvIChfKSB8IHwgIHwgICA8XF9fIFwgfCB8IHwgKF8pIHwgfF8pIHwKICAgICBcXy9cXy8gXF9fXy98X3wgIHxffFxfXF9fXy9ffCB8X3xcX19fL3wgLl9fLyAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHxffCAgICA= | base64 -d" >> /info.sh
RUN echo "echo '\n\nWelcome to the insurance-prediction example'" >> /info.sh
RUN echo "echo 'You can run the training using\n\tpoetry run train --dataset ./datasets/insurance_prediction/ --model /output/model.h5'" >> /info.sh
RUN echo "echo 'You can run the validation using\n\tpoetry run validate --dataset ./datasets/insurance_prediction/ --model /output/model.h5'" >> /info.sh
RUN echo "echo 'You can run the tests using\n\tpytest -q'" >> /info.sh
RUN echo "echo 'You can run the linting using\n\tpylint ./src ./tests'" >> /info.sh
RUN echo "echo;echo" >> /info.sh
RUN echo "echo 'Your current directory is $(pwd)'" >> /info.sh
RUN echo "echo" >> /info.sh
RUN echo "echo 'The directory contains the following directories:'" >> /info.sh
RUN echo "ls -d */" >> /info.sh
RUN echo "echo" >> /info.sh
RUN echo "echo 'The directory contains the following files:'" >> /info.sh
RUN echo "ls -p | grep -v / | tr '\n' ' '; echo" >> /info.sh
RUN echo "echo;echo" >> /info.sh
RUN echo "echo '\nTo show this info again type ""info""'" >> /info.sh
RUN chmod +x /info.sh

RUN echo 'alias info=/info.sh' > /root/.bashrc

RUN echo '#!/bin/bash' > /entrypoint.sh
RUN echo 'export REFERENCE_PATH=./datasets/insurance_prediction/reference.csv.gz' >> /entrypoint.sh
RUN echo '/info.sh' >> /entrypoint.sh
RUN echo bash >> /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
